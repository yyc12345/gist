// ==UserScript==
// @name         intervalIndex
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Save indexes of all window.setInterval
// @author       Jimmy Ben Klieve
// @match        https://mooc1-1.chaoxing.com/mycourse/studentstudy?*
// @match        https://mooc1-1.chaoxing.com/ananas/modules/video/index.html?*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    const ninjaSetInterval = window.setInterval;
    const ninjaClearInterval = window.clearInterval;

    const ninjAddEventListener = window.addEventListener;
    const ninjRemoveEventListener = window.removeEventListener;

    window.intervals = [];
    window.mouseoutEvents = [];
    window.setInterval = function (callback, timeout) {
        const id = ninjaSetInterval(callback, timeout);

        window.intervals[id] = {
            callback,
            timeout,
            id,
        };

        return id;
    }

    window.clearInterval = function (id) {
        Reflect.deleteProperty(window.intervals, id);

        ninjaClearInterval(id);
    }

    window.addEventListener = function(event, handler, capture) {
        if (event == 'mouseout') {
            window.mouseoutEvents.push(handler);
        }
        ninjAddEventListener(event, handler, capture);
    }

    window.removeEventListener = function(event, handler, options) {
        if (event == 'mouseout') {
            window.mouseoutEvents.splice(handler, 1);
        }
        ninjRemoveEventListener(event, handler, options);
    }
})();