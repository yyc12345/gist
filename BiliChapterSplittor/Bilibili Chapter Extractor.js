// ==UserScript==
// @name         Bilibili Chapter Extractor
// @namespace    http://tampermonkey.net/
// @version      2024-09-30
// @description  try to take over the world!
// @author       You
// @include      *://www.bilibili.com/video/av*
// @include      *://www.bilibili.com/video/BV*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function extractChapter() {
        let chapterPanel = document.querySelector("div.bpx-player-viewpoint");
        let chapterList = chapterPanel.querySelector("div.bpx-player-viewpoint-body>ul.bpx-player-viewpoint-menu");
        let chapterItems = chapterList.querySelectorAll("li.bpx-player-viewpoint-menu-item");

        let result = [];
        for (let i = 0; i < chapterItems.length; ++i) {
            let item = chapterItems[i];
            let chapterInfo = item.querySelector("div.bpx-player-viewpoint-menu-item-info");

            let nameNode = chapterInfo.querySelector("div.bpx-player-viewpoint-menu-item-content");
            let timeNode = chapterInfo.querySelector("div.bpx-player-viewpoint-menu-item-time");

            let nameResult = nameNode.innerText;
            let timeResult = timeNode.innerText;

            result.push(timeResult + " " + nameResult);
        }

        let joined_result = result.join("\n");
        console.log(joined_result);
        window.alert(joined_result);
    }

    let insertPoint = document.querySelector("div.danmaku-wrap");
    if (insertPoint != null) {
        var fuckingButton = document.createElement("button");
        fuckingButton.innerText = "抽取章节说明";
        fuckingButton.setAttribute("style", "height: 3em; padding: 0.5em;background: #1e90ff;color: white; border: solid 1px gray;border-radius: 5px;");
        fuckingButton.addEventListener("click", function() {
            extractChapter();
        });
        insertPoint.appendChild(fuckingButton);
    }

})();