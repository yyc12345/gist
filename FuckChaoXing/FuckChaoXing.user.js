// ==UserScript==
// @name         FuckChaoXing
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Fuck ChaoXing, need intervalIndex
// @author       yyc12345
// @match        https://mooc1-1.chaoxing.com/mycourse/studentstudy?*
// @grant        none
// ==/UserScript==

(function() {
  'use strict';

    // ================================ this is stack function
    window.fuckingChaoXing = {};
    window.fuckingChaoXing.getFunctionName = function(func) {
        if ( typeof func == 'function' || typeof func == 'object' ) {
            var name = ('' + func).match(/function\s*([\w\$]*)\s*\(/);
        }
        return name && name[1];
    }
    window.fuckingChaoXing.callstack = function() {
        var stack = [];
        var caller = arguments.callee.caller;
        while (caller) {
            stack.unshift(window.fuckingChaoXing.getFunctionName(caller));
            caller = caller && caller.caller;
        }
        return stack;
    };

    // ================================ nitification
    window.fuckingChaoXing.notification = {};
    window.fuckingChaoXing.notification.allow = undefined;
    window.fuckingChaoXing.notification.funcStop = function() {
        if (typeof(window.fuckingChaoXing.notification.allow) != 'undefined' && window.fuckingChaoXing.notification.allow) {
            var notification = new Notification("视频结束，请切换课程！");
        }
    }
    window.fuckingChaoXing.notification.funcPause = function() {
        if (typeof(window.fuckingChaoXing.notification.allow) != 'undefined' &&window.fuckingChaoXing.notification.allow) {
            var notification = new Notification("视频暂停，请回答题目！");
        }
    }
    window.fuckingChaoXing.notification.funcCheck = function() {
        if (typeof(window.fuckingChaoXing.notification.allow) == 'undefined') {
            // 先检查浏览器是否支持
            if (!("Notification" in window)) {
                window.fuckingChaoXing.notification.allow = false;
            }

            // 检查用户是否同意接受通知
            else if (Notification.permission === "granted") {
                // If it's okay let's create a notification
                window.fuckingChaoXing.notification.allow = true;
                return;
            }

            // 否则我们需要向用户获取权限
            else if (Notification.permission !== "denied") {
                Notification.requestPermission().then(function (permission) {
                    // 如果用户接受权限，我们就可以发起一条消息
                    if (permission === "granted") {
                        window.fuckingChaoXing.notification.allow = true;
                        return;
                    }
                });
            }

            window.fuckingChaoXing.notification.allow = false;
        }
    }

    // ================================ video detectator
    window.fuckingChaoXing.update = function() {
        window.fuckingChaoXing.videos = [];
        var mainIframe = document.querySelector('iframe');
        var videosIframe =mainIframe.contentDocument.querySelectorAll('iframe');
        console.log("Detected video count: " + videosIframe.length);
        for(var item = 0; item < videosIframe.length; item++) {
            var itemDocument = videosIframe[item].contentDocument;
            var itemWindow = videosIframe[item].contentWindow;
            var videoElement = itemDocument.querySelector('video');
            window.fuckingChaoXing.videos.push({
                videoObj: itemWindow.videojs.getPlayer(videoElement),
                setInterval: itemWindow.intervals,
                window: itemWindow,
                document: itemDocument,
            });
        }
    }

    // ================================ button adder
    var fuckingButton = document.createElement("button");
    fuckingButton.innerText = "超星，我日你先人";
    fuckingButton.setAttribute("style", "height: 3em; padding: 0.5em;background: #1e90ff;color: white; border: solid 1px gray;border-radius: 5px;");
    fuckingButton.addEventListener("click", function() {
        window.fuckingChaoXing.update();

        // check notification
        window.fuckingChaoXing.notification.funcCheck();

        // first, try remove mouseout event, clone it
        var mouseoutEventList = window.mouseoutEvents.concat();
        for(var q = 0; q < mouseoutEventList.length; q++) {
            window.removeEventListener('mouseout', mouseoutEventList[q]);
        }

        var successCount = 0;
        // now, try remove all limited requirements
        for(var i = 0; i < window.fuckingChaoXing.videos.length; i++) {
            let setIntervalList = window.fuckingChaoXing.videos[i].setInterval;
            for(var j in setIntervalList) {
                // add notification step
                window.fuckingChaoXing.videos[i].videoObj.on('ended', window.fuckingChaoXing.notification.funcStop);
                window.fuckingChaoXing.videos[i].videoObj.on('pause', window.fuckingChaoXing.notification.funcPause);

                // delete interval step
                let item = setIntervalList[j];
                if (item.timeout == 1000 && item.callback.name == 'n') {
                    // this one is shit interval, shutdown it
                    window.fuckingChaoXing.videos[i].videoObj.clearInterval(item.id);
                    successCount++;
                    break;
                }
            }
        }

        fuckingButton.innerText = "仙人已乘黄鹤去：共" + window.fuckingChaoXing.videos.length + "个视频，处理了" + successCount + "个";
        window.setTimeout(function() {
            // restore text
            fuckingButton.innerText = "超星，我日你先人";
        }, 10000);
    });
    document.querySelector('#mainid').parentNode.insertBefore(fuckingButton, document.querySelector('#mainid'));

})();