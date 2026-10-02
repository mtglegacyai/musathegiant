/*
 * MTG Bitcoin DCA Calculator: calculation engine and data loaders.
 *
 * Pure functions (dates, schedule, simulation) have no browser dependencies, so they
 * are unit tested in Node. Network access goes through an injected getJSON(url) helper.
 *
 * Method notes (also shown to visitors on the page):
 *  - Dates are plain "YYYY-MM-DD" strings handled with UTC calendar maths only, so a
 *    visitor's timezone can never shift a purchase date.
 *  - Each purchase is priced at that day's opening BTC/USD price (00:00 UTC).
 *  - ZAR prices = BTC/USD x that day's USD/ZAR reference rate (carried forward over weekends).
 *  - The estimated fee is a percentage taken from each purchase before buying Bitcoin.
 *  - Nothing is rounded during the calculation. Rounding happens only when displaying.
 */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.DCA = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  var MS_DAY = 86400000;
  var MAX_PURCHASES = 1200;
  /* Earliest start date offered. Coinbase daily history is checked against this. */
  var MIN_DATE = '2016-01-01';

  function DCAError(code, message, extra) {
    var e = new Error(message);
    e.name = 'DCAError';
    e.code = code;
    if (extra) for (var k in extra) e[k] = extra[k];
    return e;
  }

  /* ---------- calendar maths (UTC only, no local timezone anywhere) ---------- */
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function isLeap(y) { return (y % 4 === 0 && y % 100 !== 0) || y % 400 === 0; }
  function daysInMonth(y, m) { return [31, isLeap(y) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]; }
  function fmt(y, m, d) { return y + '-' + pad(m) + '-' + pad(d); }

  function parseISO(s) {
    if (typeof s !== 'string') return null;
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
    if (!m) return null;
    var y = +m[1], mo = +m[2], d = +m[3];
    if (mo < 1 || mo > 12 || d < 1 || d > daysInMonth(y, mo)) return null;
    return { y: y, m: mo, d: d };
  }
  function toDayNum(s) { var p = parseISO(s); return Math.round(Date.UTC(p.y, p.m - 1, p.d) / MS_DAY); }
  function fromDayNum(n) { var t = new Date(n * MS_DAY); return fmt(t.getUTCFullYear(), t.getUTCMonth() + 1, t.getUTCDate()); }
  function addDays(s, n) { return fromDayNum(toDayNum(s) + n); }
  /* Always counted from the ORIGINAL start date, so 31 Jan -> 28 Feb -> 31 Mar (no drift). */
  function addMonths(s, n) {
    var p = parseISO(s), t = p.y * 12 + (p.m - 1) + n;
    var y = Math.floor(t / 12), m = (t % 12) + 1;
    return fmt(y, m, Math.min(p.d, daysInMonth(y, m)));
  }
  function diffDays(a, b) { return toDayNum(b) - toDayNum(a); }

  /* Every purchase date from start to end (inclusive), weekly or monthly. */
  function schedule(start, end, freq) {
    if (!parseISO(start) || !parseISO(end)) throw DCAError('BAD_DATE', 'Invalid date');
    if (freq !== 'weekly' && freq !== 'monthly') throw DCAError('BAD_FREQ', 'Invalid frequency');
    var out = [], i = 0, cur = start;
    while (cur <= end) {
      out.push(cur);
      if (out.length > MAX_PURCHASES) throw DCAError('TOO_MANY', 'Too many purchases', { max: MAX_PURCHASES });
      i++;
      cur = freq === 'weekly' ? addDays(start, 7 * i) : addMonths(start, i);
    }
    return out;
  }

  /* ---------- price series ---------- */
  /* obj: { "YYYY-MM-DD": number }. Returns a sorted series for date lookups. */
  function makeSeries(obj) {
    var dates = Object.keys(obj).sort();
    var vals = new Array(dates.length);
    for (var i = 0; i < dates.length; i++) vals[i] = obj[dates[i]];
    return { dates: dates, vals: vals };
  }
  /* Value on `date`, or the latest earlier value within maxGap days. null if none. */
  function seriesAt(series, date, maxGap) {
    var lo = 0, hi = series.dates.length - 1, idx = -1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1;
      if (series.dates[mid] <= date) { idx = mid; lo = mid + 1; } else hi = mid - 1;
    }
    if (idx < 0) return null;
    if (diffDays(series.dates[idx], date) > maxGap) return null;
    return series.vals[idx];
  }

  /* ---------- validation ---------- */
  /* Returns { ok, errors:{field:message}, values } . `todayISO` is the latest allowed date. */
  function validate(input, todayISO) {
    var errors = {}, v = {};
    var amountRaw = String(input.amount == null ? '' : input.amount).replace(/[\s,]/g, '');
    var amount = amountRaw === '' ? NaN : Number(amountRaw);
    if (amountRaw === '') errors.amount = 'Enter how much you want to invest each time.';
    else if (!isFinite(amount) || amount <= 0) errors.amount = 'Enter an amount greater than 0.';
    else if (amount > 1e9) errors.amount = 'That amount is too large. Try a smaller number.';
    v.amount = amount;

    v.currency = input.currency === 'USD' ? 'USD' : (input.currency === 'ZAR' ? 'ZAR' : null);
    if (!v.currency) errors.currency = 'Choose ZAR or USD.';
    v.freq = input.freq === 'weekly' ? 'weekly' : (input.freq === 'monthly' ? 'monthly' : null);
    if (!v.freq) errors.freq = 'Choose weekly or monthly.';

    var feeRaw = String(input.feePct == null ? '' : input.feePct).replace(/[\s,]/g, '').replace(/%$/, '');
    var fee = feeRaw === '' ? 0 : Number(feeRaw);
    if (!isFinite(fee) || fee < 0) errors.feePct = 'Enter a fee of 0 or more, or leave it blank.';
    else if (fee > 20) errors.feePct = 'A fee above 20% looks like a typing mistake. Please check it.';
    v.feePct = fee;

    v.start = input.start; v.end = input.end;
    if (!input.start) errors.start = 'Choose a start date.';
    else if (!parseISO(input.start)) errors.start = 'That start date is not valid.';
    else if (input.start < MIN_DATE) errors.start = 'Price history starts on ' + MIN_DATE + '. Choose a later start date.';
    else if (input.start > todayISO) errors.start = 'The start date cannot be in the future.';

    if (!input.end) errors.end = 'Choose an end date.';
    else if (!parseISO(input.end)) errors.end = 'That end date is not valid.';
    else if (input.end > todayISO) errors.end = 'The end date cannot be in the future.';
    else if (!errors.start && input.end < input.start) errors.end = 'The end date must be on or after the start date.';

    var ok = Object.keys(errors).length === 0;
    if (ok) {
      try { schedule(v.start, v.end, v.freq); }
      catch (e) {
        if (e.code === 'TOO_MANY') errors.end = 'That range has more than ' + MAX_PURCHASES + ' purchases. Choose monthly or a shorter range.';
        ok = false;
      }
    }
    return { ok: ok && Object.keys(errors).length === 0, errors: errors, values: v };
  }

  /* ---------- the calculation ---------- */
  /*
   * p: { amount, freq, start, end, feePct, currency,
   *      btcUsd: series (BTC price in USD by date), usdZar: series (ZAR per 1 USD) or null,
   *      nowPrice: current BTC price in the chosen currency, nowDate: ISO date of "today" }
   */
  function simulate(p) {
    var dates = schedule(p.start, p.end, p.freq);
    var feeRate = (p.feePct || 0) / 100;
    var useZar = p.currency === 'ZAR';

    function priceOn(date) {
      var usd = seriesAt(p.btcUsd, date, 4);
      if (usd == null || !(usd > 0)) throw DCAError('NO_PRICE', 'No Bitcoin price for ' + date, { date: date });
      if (!useZar) return usd;
      var fx = seriesAt(p.usdZar, date, 10);
      if (fx == null || !(fx > 0)) throw DCAError('NO_FX', 'No exchange rate for ' + date, { date: date });
      return usd * fx;
    }

    var contributed = 0, netTotal = 0, feesPaid = 0, btc = 0;
    var rows = [], series = [];
    for (var i = 0; i < dates.length; i++) {
      var price = priceOn(dates[i]);
      var fee = p.amount * feeRate;
      var net = p.amount - fee;
      var bought = net / price;
      contributed += p.amount; netTotal += net; feesPaid += fee; btc += bought;
      rows.push({ date: dates[i], price: price, spent: p.amount, fee: fee, btcBought: bought, btcTotal: btc, contributed: contributed, value: btc * price });
      series.push({ date: dates[i], contributed: contributed, value: btc * price });
    }

    var n = dates.length;
    var currentValue = btc * p.nowPrice;
    var profit = currentValue - contributed;
    var returnPct = contributed > 0 ? (profit / contributed) * 100 : 0;
    var avgPrice = btc > 0 ? netTotal / btc : 0; /* average market price paid, before fees */

    /* The chart covers the chosen period only, so it ends on the end date.
       If the end date is today, the last point uses the live price. If it is in the past,
       the last point is valued at that day's price (the "current value" tiles still use today's price). */
    var last = series[series.length - 1];
    if (p.end === p.nowDate) {
      if (last.date === p.end) { last.value = currentValue; rows[rows.length - 1].value = currentValue; last.today = true; }
      else series.push({ date: p.end, contributed: contributed, value: currentValue, today: true });
    } else if (last.date < p.end) {
      series.push({ date: p.end, contributed: contributed, value: btc * priceOn(p.end), endPoint: true });
    }

    /* Lump sum: the same total money, invested once on the start date (one fee). */
    var startPrice = rows[0].price;
    var lumpFee = contributed * feeRate;
    var lumpBtc = (contributed - lumpFee) / startPrice;
    var lumpValue = lumpBtc * p.nowPrice;
    var lumpProfit = lumpValue - contributed;

    return {
      currency: p.currency, freq: p.freq, start: p.start, end: p.end, nowDate: p.nowDate,
      purchases: n, contributed: contributed, feesPaid: feesPaid, btc: btc, avgPrice: avgPrice,
      nowPrice: p.nowPrice, currentValue: currentValue, profit: profit, returnPct: returnPct,
      lump: { btc: lumpBtc, startPrice: startPrice, value: lumpValue, profit: lumpProfit,
              returnPct: contributed > 0 ? (lumpProfit / contributed) * 100 : 0, fee: lumpFee,
              diff: currentValue - lumpValue },
      rows: rows, series: series
    };
  }

  /* ---------- data loading (browser). getJSON(url) -> Promise<json> ---------- */
  var CB = 'https://api.exchange.coinbase.com';
  var FX = 'https://api.frankfurter.dev/v1';

  function pool(tasks, limit) {
    return new Promise(function (resolve, reject) {
      var results = new Array(tasks.length), next = 0, active = 0, done = 0, failed = false;
      if (!tasks.length) return resolve(results);
      function run() {
        while (!failed && active < limit && next < tasks.length) {
          (function (i) {
            active++;
            tasks[i]().then(function (r) { results[i] = r; active--; done++; if (done === tasks.length) resolve(results); else run(); },
                            function (e) { failed = true; reject(e); });
          })(next++);
        }
      }
      run();
    });
  }
  function withRetry(fn, tries) {
    return fn().catch(function (e) {
      if (tries <= 0) throw e;
      return new Promise(function (r) { setTimeout(r, 900); }).then(function () { return withRetry(fn, tries - 1); });
    });
  }

  /* Daily BTC/USD opens from Coinbase Exchange public candles (max 300 per request). */
  function loadBtcUsd(start, end, getJSON) {
    var chunks = [], cs = start;
    while (cs <= end) {
      var ce = addDays(cs, 289); if (ce > end) ce = end;
      chunks.push([cs, ce]);
      cs = addDays(ce, 1);
    }
    var tasks = chunks.map(function (c) {
      return function () {
        var url = CB + '/products/BTC-USD/candles?granularity=86400&start=' + c[0] + 'T00:00:00Z&end=' + c[1] + 'T00:00:00Z';
        return withRetry(function () { return getJSON(url); }, 2);
      };
    });
    return pool(tasks, 3).then(function (parts) {
      var map = {}, count = 0;
      parts.forEach(function (rows) {
        if (!Array.isArray(rows)) throw DCAError('BAD_DATA', 'Unexpected price data');
        rows.forEach(function (r) {
          /* [time, low, high, open, close, volume] */
          var o = Number(r[3]);
          if (!(o > 0)) return;
          map[fromDayNum(Math.floor(r[0] / 86400))] = o; count++;
        });
      });
      if (!count) throw DCAError('NO_DATA', 'No Bitcoin price data returned');
      return map;
    });
  }

  /* Daily USD -> ZAR reference rates (ECB data via Frankfurter), business days only. */
  function loadUsdZar(start, end, getJSON) {
    var from = addDays(start, -10), chunks = [], cs = from;
    while (cs <= end) {
      var ce = addDays(cs, 365 * 3); if (ce > end) ce = end;
      chunks.push([cs, ce]);
      cs = addDays(ce, 1);
    }
    var tasks = chunks.map(function (c) {
      return function () {
        var url = FX + '/' + c[0] + '..' + c[1] + '?base=USD&symbols=ZAR';
        return withRetry(function () { return getJSON(url); }, 2);
      };
    });
    return pool(tasks, 2).then(function (parts) {
      var map = {}, count = 0;
      parts.forEach(function (j) {
        var r = j && j.rates;
        if (!r) throw DCAError('BAD_DATA', 'Unexpected exchange rate data');
        Object.keys(r).forEach(function (d) { var z = r[d] && Number(r[d].ZAR); if (z > 0) { map[d] = z; count++; } });
      });
      if (!count) throw DCAError('NO_DATA', 'No exchange rate data returned');
      return map;
    });
  }

  /* Current BTC/USD and (for ZAR) USD/ZAR, each with a fallback source. */
  function loadNow(currency, getJSON) {
    var btc = getJSON(CB + '/products/BTC-USD/ticker').then(function (j) {
      var p = Number(j && j.price); if (!(p > 0)) throw new Error('bad ticker');
      return { price: p, at: j.time ? Date.parse(j.time) : Date.now(), src: 'Coinbase' };
    }).catch(function () {
      return getJSON('https://api.coinbase.com/v2/prices/BTC-USD/spot').then(function (j) {
        var p = Number(j && j.data && j.data.amount); if (!(p > 0)) throw new Error('bad spot');
        return { price: p, at: Date.now(), src: 'Coinbase' };
      });
    });
    var fx = currency !== 'ZAR' ? Promise.resolve(null) :
      getJSON(FX + '/latest?base=USD&symbols=ZAR').then(function (j) {
        var z = Number(j && j.rates && j.rates.ZAR); if (!(z > 0)) throw new Error('bad fx');
        return { rate: z, date: j.date, src: 'European Central Bank via Frankfurter' };
      }).catch(function () {
        return getJSON('https://open.er-api.com/v6/latest/USD').then(function (j) {
          var z = Number(j && j.rates && j.rates.ZAR); if (!(z > 0)) throw new Error('bad fx2');
          return { rate: z, date: null, src: 'ExchangeRate-API' };
        });
      });
    return Promise.all([btc, fx]).then(function (r) {
      return { btcUsd: r[0].price, at: r[0].at, btcSrc: r[0].src, usdZar: r[1] ? r[1].rate : null, fxSrc: r[1] ? r[1].src : null, fxDate: r[1] ? r[1].date : null };
    });
  }

  return {
    MIN_DATE: MIN_DATE, MAX_PURCHASES: MAX_PURCHASES, DCAError: DCAError,
    isLeap: isLeap, daysInMonth: daysInMonth, parseISO: parseISO, addDays: addDays, addMonths: addMonths, diffDays: diffDays,
    schedule: schedule, makeSeries: makeSeries, seriesAt: seriesAt, validate: validate, simulate: simulate,
    loadBtcUsd: loadBtcUsd, loadUsdZar: loadUsdZar, loadNow: loadNow, fromDayNum: fromDayNum
  };
});
