const COOKIES_NAME_COUNT = "advice_count_load";
const COOKIES_NAME_LAST_NUMBER = "advice_last_number_load";
const COOKIES_NAME_WIDGETS_LENGTH = "advice_widgets_length";
const COOKIES_TIME_LIFE = 5; // 5 hours

class ShuffleAdvice {
  constructor(jquery) {
    this.$ = jquery;
  }

  addEvent() {
    const $ = this.$;
    if ($(".commercial-block").length > 0) {
      this.updateAdviceCountLoad();
      this.getNextNumber();
    }
  }

  updateAdviceCountLoad() {
    let countLoad = this.getCookieNameCount();
    countLoad++;
    this.setCookieNameCount(countLoad);
  }


  /*************GET*********************/

  getNextNumber() {
    const countLoad = this.getCookieNameCount();
    const currentNumber = this.getCookieNameLastNumber();
    const maxNumber = this.getCookieNameWidgetsLength();
    if (maxNumber > 4) {
      switch (true) {
        case (countLoad < 4):
          this.setCookieNameLastNumber(this.getNumber(1, 4, currentNumber));
          break;
        case (countLoad >= 4  && countLoad < 7):
          if (maxNumber > 6) {
            this.setCookieNameLastNumber(this.getNumber(4, 6, false));
          } else {
            this.setCookieNameLastNumber(this.getNumber(3, 5, false));
          }
          break;
        default:
          this.setCookieNameLastNumber(0);
          break;
      }
    } else {
      this.setCookieNameLastNumber(0);
    }
  }

  getNumber(min, max, last = false) {
    const k = this.randomInteger(min, max);
    return (!last || k !== last) ? k : this.getNumber(min, max, last);
  }

  getCookieNameCount() {
    const count = parseInt(this.getCookie(COOKIES_NAME_COUNT));
    return count || 0;
  }

  getCookieNameLastNumber() {
    const count = parseInt(this.getCookie(COOKIES_NAME_LAST_NUMBER));
    return count || false;
  }

  getCookieNameWidgetsLength() {
    const count = parseInt(this.getCookie(COOKIES_NAME_WIDGETS_LENGTH));
    return count || 0;
  }

  getCookie(name) {
    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : false;
  }

  getCookieDate()
  {
    const date = new Date();
    date.setHours(date.getHours() + COOKIES_TIME_LIFE);
    return date;
  }

  /*************END*GET*********************/

  /*************SET*********************/

  setCookieNameCount(count) {
    this.setCookie(COOKIES_NAME_COUNT, count, this.getCookieDate(), "/");
  }

  setCookieNameLastNumber(number) {
    this.setCookie(COOKIES_NAME_LAST_NUMBER, number, this.getCookieDate(), "/");
  }

  setCookie(name, value, date, path, domain, secure) {
    let cookie_string = name + "=" + escape(value);
    if (date) {
      const expires = date;
      cookie_string += "; expires=" + expires.toGMTString();
    }
    if (path) {
      cookie_string += "; path=" + escape(path);
    }

    if (domain) {
      cookie_string += "; domain=" + escape(domain);
    }

    if (secure) {
      cookie_string += "; secure";
    }

    document.cookie = cookie_string;
  }

  /*************END*SET*********************/

  randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

}

