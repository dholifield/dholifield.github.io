window.__tnt || (window.__tnt = {});

/*
__tnt.appName = 'TownNews Templates';
__tnt.appVersion = '0.1.0.0';
*/

__tnt.client = ( function( window, undefined ) {
    this.obj = {};

    this.obj.userAgent = navigator.userAgent.toLowerCase();

    this.obj.browser = {
        name: (function() {
            var userAgent = navigator.userAgent;
            if (userAgent.indexOf('Chrome') !== -1 &&
                userAgent.indexOf('Chromium') == -1 &&
                userAgent.indexOf('OPR') == -1 &&
                userAgent.indexOf('Edge') == -1 &&
                userAgent.indexOf('SamsungBrowser') == -1) return 'Chrome';
            if (userAgent.indexOf('Safari') !== -1 &&
                userAgent.indexOf('Chrome') == -1 &&
                userAgent.indexOf('Chromium') == -1 &&
                userAgent.indexOf('Android') == -1) return 'Safari';
            if (userAgent.indexOf('Firefox') !== -1 &&
                userAgent.indexOf('Seamonkey') == -1) return 'Firefox';
            if (/trident/i.test(userAgent)) return 'IE';
            if (userAgent.indexOf('OPR') !== -1) return 'Opera';
            if (userAgent.indexOf('SamsungBrowser') !== -1) return 'Samsung Internet';
            if (userAgent.indexOf('Edge') !== -1 &&
                userAgent.indexOf('Chrome') !== -1) return 'Edge';
            return 'Other';
        })()
    };

    this.obj.browser.version = (function() {
        if (this.obj.browser.name == 'Other') return;
        var name = this.obj.browser.name + '/',
            start = navigator.userAgent.indexOf(name),
            preNum = navigator.userAgent.substring(start + name.length),
            index = preNum.indexOf(' ');
        if (index > 0) preNum = preNum.substring(0, index);
        var end = (preNum.indexOf('.', 2) > 0) ? preNum.indexOf('.', 2) : preNum.indexOf('.', 1),
            num = preNum.substring(0, end);
        return Number(num);
    })();

    this.obj.platform = window["eb.platform"] = {
        win:/win/.test(this.obj.userAgent),
        mac:/mac/.test(this.obj.userAgent),
        touchDevice: (function(){
            try {
                return 'ontouchstart' in document.documentElement;
            } catch (e) {
                return false;
            } 
        })(),
        android: (this.obj.userAgent.indexOf("android") > -1),
        ipad: (this.obj.userAgent.match(/ipad/i) ? true : false),
        iphone: (this.obj.userAgent.match(/iphone/i) ? true : false),
        ipod: (this.obj.userAgent.match(/ipod/i) ? true : false),
        winphone: (this.obj.userAgent.match(/Windows Phone/i) ? true : false),
        blackberry: (this.obj.userAgent.match(/BlackBerry/i) ? true : false),
        webos: (this.obj.userAgent.match(/webOS/i) ? true : false)
    };
    this.obj.platform.ios = ( this.obj.platform.ipad || this.obj.platform.ipod || this.obj.platform.iphone );

    this.obj.touchOnly = this.obj.platform.touchDevice && (this.obj.platform.android || this.obj.platform.ios || this.obj.platform.winphone || this.obj.platform.blackberry || this.obj.platform.webos || this.obj.platform.silk );

    this.obj.clickEvent = ( this.obj.touchOnly ) ? 'touchend' : 'click';

    this.obj.capabilities = {
            supportsCookies: (navigator.cookieEnabled) ? true : false,
            supportsLocalStorage: function() {
                var test = 'test';
                try {
                    localStorage.setItem(test, test);
                    localStorage.removeItem(test);
                    return true;
                } catch(e) {
                    return false;
                }
            },
            supportsFlash: function(){
            }
        }

    return this.obj;
} )( window );

__tnt.user = ( function( window, undefined ) {
    this.obj = {
        authToken: (TNCMS.User.isLoggedIn()) ? true : null,
        screenName: TNCMS.User.getScreenName(),
        avatar: Cookies.get('tncms-avatarurl'),
        remember: TNCMS.User.hasPersistentSession(),
        services: Cookies.get('tncms-services'),
        update: function(){
            /* Update user object data */
            __tnt.user.loggedIn = (TNCMS.User.isLoggedIn()) ? true : null; 
            __tnt.user.authToken = (TNCMS.User.isLoggedIn()) ? true : null;
            __tnt.user.screenName = Cookies.get('tncms-screenname');
            __tnt.user.remember = TNCMS.User.hasPersistentSession();
            __tnt.user.services = Cookies.get('tncms-services');
            
            /* fire userStatus event */
            if(__tnt && __tnt.subscription && __tnt.subscription.access && __tnt.subscription.access.status){
               __tnt.subscription.access.status.data = null;
               __tnt.subscription.access.status.trigger(userStatus);
            }
        }
    };
    this.obj.loggedIn = TNCMS.User.isLoggedIn();
    
    return this.obj;
} )( window );

__tnt.log = function( obj ) {
    if( window.console ) console.log(obj);
}

/** get a url hash param */
__tnt.urlHash = function( p ) {
     var pRegex = new RegExp("#.*[?&]" + p + "=([^&]+)(&|$)");
     var pMatch = location.href.match(pRegex);
     return pMatch ? pMatch[1] : '';
}

/** set default author validation as false */
__tnt.isAuthor = false;
document.addEventListener('DOMContentLoaded', function() {
    if (document.body.dataset.authors !== undefined) {
        var authors = JSON.parse(document.body.dataset.authors);
        if (__tnt.user.loggedIn && authors.indexOf(__tnt.user.screenName) !== -1) {
            __tnt.isAuthor = true;
        }
    }
});

__tnt.trackEventLater = [];
__tnt.trackEvent = function( obj ) {
    if( jQuery.type(obj) === 'object' ){
        __tnt.trackEventLater.push(obj);
    }
}

/** string truncate */
__tnt.truncateStr = function(sContent, iLen, sAppend) {
    if( sContent.length > iLen ){
        sAppend = sAppend ? sAppend : '';
        sContent = sContent.substring(0,iLen)+sAppend;
    }
    return sContent;
}

/** 
 * compare array
 * @description Returns true if any source item matches a target
 */
__tnt.compareArray = function (source, target) {
    if (typeof source == 'undefined' || typeof target == 'undefined') return;
    if (typeof source == 'string') source = JSON.parse(source);
    var result = source.filter(function(item){ return target.indexOf(item) > -1});
    return (result.length > 0);
}

/** 
 * shuffle array
 * @description Shuffles and returns an array
 */
__tnt.shuffleArray = function(array) {
    var currentIndex = array.length, temporaryValue, randomIndex;
    // While there remain elements to shuffle
    while (0 !== currentIndex) {
        // Pick a remaining element
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;
        // And swap it with the current element
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }
    return array;
}

/** check if element is in viewport */
__tnt.elementOnScreen = function(sElem, iThreshold) {
    if( $(sElem).length === 0 ) { return false; }
    var $e = $(sElem);
    var $w = $(window);
    var iThreshold = iThreshold ? iThreshold : 5;
    var docViewTop = $w.scrollTop();
    var docViewBottom = docViewTop + $w.height();
    var elemTop = $e.offset().top - iThreshold;
    var elemBottom = elemTop + $e.height() - iThreshold;
    return (docViewBottom >= elemTop && docViewTop <= elemBottom);
}

/** get outer height of element */
__tnt.outerHeight = function(elem, includeMargin) {
    var e, eHeight, eMargin = 0;
    if (typeof elem === 'string'){
        e = document.querySelector(elem);
    } else if (typeof elem === 'object') {
        e = elem;
    };
    if (e !== null){
        eHeight = e.offsetHeight;
        if (includeMargin === true) {
            eMargin = parseInt(document.defaultView.getComputedStyle(e, '').getPropertyValue('margin-top')) 
                + parseInt(document.defaultView.getComputedStyle(e, '').getPropertyValue('margin-bottom'));
        } return (eHeight + eMargin);
    } return 0;
}

/** DMP */
__tnt.dmp = {};

/** Audience extraction event */
__tnt.dmp.audienceExtracted = function(audience) {
    var event = new CustomEvent('tnt-dmp-audience-extracted', {detail: {userAudience: audience}});
    window.dispatchEvent(event);

    // Temporary - Store audience within localStorage
    if (__tnt.client.capabilities.supportsLocalStorage() && localStorage.getItem('tncms.dmp.audiences') !== JSON.stringify(audience)) {
        localStorage.setItem('tncms.dmp.audiences', JSON.stringify(audience));
    }
}

/** Behavioral reccomendation event */
__tnt.dmp.behaviorRec = function(audience) {
    var event = new CustomEvent('tnt-dmp-behavior-rec', {detail: {userAudience: audience}});
    window.dispatchEvent(event);
}

/** 
 * Preview check
 * @description Returns true if preview
 */
__tnt.isPreview = function () {
    return window.location.pathname.indexOf('/tncms/admin/action/main/preview/site');
}

/** Rewrite URL for preview */
__tnt.scrubUrl = function(sUrl) {
    // live mode
    if (location.href.indexOf('tncms/admin') == -1) {
        return sUrl;
    // preview mode
    } else {
        var sDomain = location.href.split('/')[3],
            sSecureDomain = 'https://www.'+sDomain,
            sSecureDomainNoWWW = 'https://'+sDomain,
            sNewUrl;

        var re = new RegExp('https:\/\/admin[\-\.].*?\.(com|net)\/'+sDomain, 'g');

        if (
            (
                sUrl.charAt(0) == '/'
                && sUrl.indexOf('/'+sDomain+'/tncms/admin/action/main/preview/site') == -1
            ) || (
                /^https:\/\/admin[\-\.].*?\.(com|net)/.test(sUrl) == true
                && sUrl.indexOf('/shared-content/') == -1
                && re.test(sUrl) == false
            )
        ) {
            sNewUrl = '/'+sDomain+'/tncms/admin/action/main/preview/site/-'+ sUrl.replace(/https:\/\/admin[\-\.].*?\.(com|net)/, '');

        } else if (sUrl.indexOf('http://www.'+sDomain) == 0) {
            sNewUrl = '/'+sDomain+'/tncms/admin/action/main/preview/site/-'+ sUrl.replace('http://www.'+sDomain, '');

        } else if (sUrl.indexOf(sSecureDomain) == 0) {
            sNewUrl = '/'+sDomain+'/tncms/admin/action/main/preview/site/-'+ sUrl.replace(sSecureDomain, '');

        } else if( sUrl.indexOf('us-corp-qa-3') ){ // QA3 special case
            sNewUrl = '/'+sDomain+'/tncms/admin/action/main/preview/site/-'+ sUrl.replace(sSecureDomainNoWWW, '');

        } else {
            sNewUrl = sUrl;
        }
        return sNewUrl;
    }
}

/** 
 * Preview scrub content
 * @description Returns element with links scrubbed for preview
 */
__tnt.scrubElem = function (elem, target) { 
    if (__tnt.isPreview) {
        if (!target) target = 'a';
        
        // Handle template element 
        if (elem.content) {
            var template = elem;
            elem = elem.content;
        }
        
        // Scrub links
        elem.querySelectorAll(target).forEach(function(link) { 
            let href = link.getAttribute('href');
            link.setAttribute('href', __tnt.scrubUrl(href));
        });
        
        // Update templete element
        if (template) {
            template.content = elem;
            elem = template;
        }
    }
    return elem;
}

/*
 * Template Code
 * @param template = element
 * @param insertionPoint = element
 * @param inesrtionBefore = boolean
 * @param data = array of objects [{'element':'css selector', 'html':'inserted content', 'attr':{'key':'value',}}]
 * @param callback = function(t){}
 * @param id = string, id to apply to top level element
 *
 * @description - takes a template element and inserts provided data before running a callback
 */
__tnt.template = function(template, insertionPoint, insertionBefore, data, callback) {
    var t = '';

    if(template){
        if (typeof(insertionBefore) == "undefined") {
            insertionBefore = false;
        }

        if (template.nodeName=='TEMPLATE') {
            if ("content" in document.createElement("template")) {
                t = document.importNode(template.content, true);
            } else {
                t = document.createDocumentFragment();
                var children = template.childNodes;
                for (i=0; i<children.length; i++) {
                    t.appendChild(children[i].cloneNode(true));
                }
            }

            if (Array.isArray(data)) {
                data.forEach(function(el) {
                    var element = t;
                
                    if (el) {
                        element = t.querySelectorAll(el.element);

                        if (el.first) {
                            element = element.slice(0,1);
                        }
                    }

                    if (element) {
                        if (el.attr) {
                            for (a=0; a<el.attr.length; a++) {
                                for (e=0; e<element.length; e++) {
                                    element[e].setAttribute(el.attr[a].attr, el.attr[a].value);
                                }
                            }
                        }

                        if (el.html) {
                            for (i=0; i<element.length; i++) {
                                element[i].innerHTML = el.html;
                            }
                        }
                    }
                });
            }

            if (typeof(callback)=='function') {
                callback(t);
            }

            if (insertionPoint) {
                if (insertionBefore) {
                    insertionPoint.insertBefore(t, insertionPoint.firstChild);
                } else {
                    insertionPoint.appendChild(t);
                }
            }

        } else { __tnt.log("__tnt.template - no valid template element found - update to use template tag"); }
    } else { __tnt.log("__tnt.template - no template element found"); }

    return t;
};

/**
  Youtube helper class
 */ 
__tnt.youtube = (function(window, undefined){
    var trackInterval,
        percentTracked = 0;
    o = {};
    o.create = [];
    o.playing = false;
    o.state = {
        change: function(event){
            switch(event.data){
                case YT.PlayerState.ENDED:
                    clearInterval(trackInterval);
                    break;
                case YT.PlayerState.PLAYING:

                    /** dont allow more than one video to play at a time */
                    if(event.target != o.playing) o.state.pause();
                    o.playing = event.target;
                    
                    // Track resume event
                    if (o.playing.playerInfo.currentTime > 1) {
                        o.videoDataEvent(o.playing, 'video_resumed');
                    }
                    
                    // Begin progress tracking interval
                    trackInterval = setInterval(function(){
                        o.videoDataEvent(o.playing);
                    }, 1000);
                    
                    break;
                case YT.PlayerState.PAUSED:
                    // Track paused event
                    o.videoDataEvent(o.playing, 'video_paused');
                    
                    clearInterval(trackInterval);
                    break;
            }
        },
        pause: function(){
           if (o.playing && typeof o.playing.pauseVideo === 'function') {
               o.playing.pauseVideo();
           } else {
               console.log('TNT: o.playing.pauseVideo is not available');
           }
        }
    },
    o.players = {
        register: function(id){
            if( o.create.length === 0 ){
                var _yTag = document.createElement('script');
                    _yTag.src = 'https://www.youtube.com/iframe_api';
                var _yScript = document.getElementsByTagName('script')[0];
                    _yScript.parentNode.insertBefore(_yTag, _yScript);
            }
            o.create.push(id);
        },
        init: function(){
            if(o.create.length > 0){
                __tnt.log('  Players:');
                $.each(o.create, function(i, video){
                    __tnt.log('    '+ video);
                    new YT.Player(video, {
                        events: {
                            'onStateChange': o.state.change
                        }
                    });
                    
                    /** Observe player visibility */
                    var videoElem = document.getElementById(video),
                        callback_io = function(entries, player_io) {
                        if (entries[0].isIntersecting) {
                            videoElem.dataset.visible = 'true';
                        } else {
                            videoElem.dataset.visible = 'false';
                        }
                    }
                    var player_io = new IntersectionObserver(callback_io);
                    player_io.observe(videoElem);
                });
            }
        }
    },
    o.videoDataEvent = function(player, event) {
        var eventName = '',
            eventCategory = 'video',
            eventAction = '',
            eventLabel = '',
            duration = player.playerInfo.duration,
            curTime = player.playerInfo.currentTime,
            percentComplete = Math.round(100 - ((duration - Math.floor(curTime)) / duration) * 100),
            bTrackProgress = false;
        
        if (percentComplete >= 5 && percentComplete <= 10) { percentComplete = 10; bTrackProgress = true;}
        else if (percentComplete >= 20 && percentComplete <= 25) { percentComplete = 25; bTrackProgress = true;}
        else if (percentComplete >= 45 && percentComplete <= 50) { percentComplete = 50; bTrackProgress = true;}
        else if (percentComplete >= 70 && percentComplete <= 75) { percentComplete = 75; bTrackProgress = true;}
        else if (percentComplete >= 95 && percentComplete <= 100) { percentComplete = 100; }
        
        /* Set event data */
        if (event == 'video_paused') {
            eventName = 'video_paused';
            eventAction = 'video paused';
            eventLabel = o.playing.h.dataset.title + ':' + o.playing.h.dataset.uuid;
            curTime = duration/100 * percentComplete;
        } else if (curTime <= 1){
            eventName = 'video_start';
            eventAction = 'video start';
            eventLabel = o.playing.h.dataset.title + ':' + o.playing.h.dataset.uuid;
            curTime = 0;
        } else if (percentComplete == 100) {
            // Clear inverval on completion
            clearInterval(trackInterval);
            eventName = 'video_complete';
            eventAction = 'video ended';
            eventLabel = o.playing.h.dataset.title + ':' + o.playing.h.dataset.uuid;
            curTime = duration;
        } else if (event == 'video_resumed') {
            eventName = 'video_resumed';
            eventAction = 'video resumed';
            eventLabel = o.playing.h.dataset.title + ':' + o.playing.h.dataset.uuid;
            curTime = duration/100 * percentComplete;
        } else if(bTrackProgress) {
            if (percentComplete > percentTracked) {
                percentTracked = percentComplete;
                eventName = 'video_progress';
                eventAction = 'video progress';
                eventLabel = percentComplete + ':' + o.playing.h.dataset.title + ':' + o.playing.h.dataset.uuid;
                curTime = duration/100 * percentComplete;
            } else {
                return;
            }
        } else {
            return;
        }
        
        var tntVideoData = new CustomEvent('tntVideoData', {
          detail: {
              video_uuid: o.playing.h.dataset.uuid,
              video_title: o.playing.h.dataset.title,
              video_provider: 'youtube',
              video_duration: Math.round(duration),
              video_url: player.playerInfo.videoUrl,
              video_current_time: Math.round(curTime),
              video_progress: percentComplete,
              visible: o.playing.h.dataset.visible
          }
        });
        
        // Dispatch general data event
        dispatchEvent(tntVideoData);
        
        // GTM tracking
        dataLayer.push({
            'event': 'tncms.event.trigger',
                'tncms.event.trigger.category': eventCategory,
                'tncms.event.trigger.action': eventAction,
                'tncms.event.trigger.label': eventLabel,
                'tncms.event.trigger.value': '1',
                'tncms.event.trigger.name': eventName,
                'tncms.event.trigger.video_uuid': o.playing.h.dataset.uuid,
                'tncms.event.trigger.video_title': o.playing.h.dataset.title,
                'tncms.event.trigger.video_provider': 'youtube',
                'tncms.event.trigger.video_url': player.playerInfo.videoUrl,
                'tncms.event.trigger.video_duration': Math.round(duration),
                'tncms.event.trigger.video_current_time': Math.round(curTime),
                'tncms.event.trigger.video_percent': percentComplete,
                'tncms.event.trigger.visible': o.playing.h.dataset.visible
        });
    }
    return o;
})(window);

/**
 * YoutTube API will fire onYouTubeIframeAPIReady function when the JS for the API is available
 * Fire youtube onload function when called.
 */
function onYouTubeIframeAPIReady(){
    /** 
      Wait until window load to ensure all players registered.
      For some reason attaching YT class to a player before its fully loaded, can cause event bindings to fail.
     */
    jQuery(window).load(function(){
        __tnt.log('Init YT:');
        __tnt.youtube.players.init();
    });
}
