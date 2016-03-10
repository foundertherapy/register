function loadOrganizeIframe() {
    var iframeTag = document.createElement('iframe');
    iframeTag.setAttribute('id', 'organize_iframe');
    iframeTag.setAttribute('src', 'http://127.0.0.1:8888/?widget_id=' + organizeWidgetId);
    iframeTag.setAttribute('class', 'organize-iframe');
    iframeTag.setAttribute('width', '100%');
    iframeTag.setAttribute('height', '100%');

    document.getElementById('organize_modal_content').appendChild(iframeTag);
    document.getElementById('organize_modal').setAttribute('class', 'organize-modal organize-modal-opened');
}

function closeOrganizeIframe() {
    document.getElementById('organize_modal').setAttribute('class', 'organize-modal');
    document.getElementById('organize_modal_content').removeChild(document.getElementById('organize_iframe'));
}

function popupWindow() {
    url = 'http://127.0.0.1:8888/?widget_id=' + organizeWidgetId;
    title = 'ORGANIZE / Register to become an organ donor'
    h = screen.height - screen.height * 0.1;
    w = screen.width - screen.width * 0.1;
    wLeft = (window.screenLeft ? window.screenLeft : window.screenX) + (screen.width - w) / 2;
    wTop = (window.screenTop ? window.screenTop : window.screenY) + (screen.height - h) / 2;

    var left = wLeft + (window.innerWidth / 2) - (w / 2);
    var top = wTop + (window.innerHeight / 2) - (h / 2);
    return window.open(url, title, 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=no, resizable=no, copyhistory=no, width=' + (w - w * 0.2) + ', height=' + (h - h * 0.2) + ', top=' + (top) + ', left=' + left);
}

(function() {
    var isMobile = false;
    // device detection
    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || screen.width <= 480)
    {
        isMobile = true;
    }

    var linkTag = document.createElement('link');
    linkTag.setAttribute('rel', 'stylesheet');
    linkTag.setAttribute('href', '//127.0.0.1:8888/static/css/modal.css');
    linkTag.setAttribute('type', 'text/css');
    document.getElementsByTagName('head')[0].appendChild(linkTag);

    if (isMobile == false)
    {
        var organizeModalDivTag = document.createElement('div');
        organizeModalDivTag.setAttribute('id', 'organize_modal');
        organizeModalDivTag.setAttribute('class', 'organize-modal');


        var organizeModalContentDivTag = document.createElement('div');
        organizeModalContentDivTag.setAttribute('class', 'organize-modal-content');
        organizeModalContentDivTag.setAttribute('id', 'organize_modal_content');

        var organizeModalCloseDivTag = document.createElement('div');
        organizeModalCloseDivTag.setAttribute('onclick', 'javascript: closeOrganizeIframe()');
        organizeModalCloseDivTag.setAttribute('class', 'organize-close');
        organizeModalCloseDivTag.innerHTML = '&times;';

        organizeModalContentDivTag.appendChild(organizeModalCloseDivTag);
        organizeModalDivTag.appendChild(organizeModalContentDivTag);

        document.getElementsByTagName('body')[0].appendChild(organizeModalDivTag);
    }

    var organizeRegistrationBtnTag = document.createElement('div');

    if (isMobile == false)
    {
        if (typeof organizeAlwaysOpenInPage === 'undefined' || organizeAlwaysOpenInPage == true) {
            organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: loadOrganizeIframe();');
        }
        else {
            organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: popupWindow();');
        }
    }
    else
    {
        organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: window.open(\'http://127.0.0.1:8888/?widget_id=' + organizeWidgetId + '\');');
    }

    organizeRegistrationBtnTag.setAttribute('class', 'organize-registration-btn');
    organizeRegistrationBtnTag.setAttribute('id', 'organize_registration_btn');
    var widgetChoiceImagePath = "//127.0.0.1:8888/static/images/widget/" + organizeWidgetChoice + ".png";
    organizeRegistrationBtnTag.innerHTML = '<img style="height: 100%;border:1px solid #021a40;" src="' + widgetChoiceImagePath + '"/>';

    organizeScriptNode = document.getElementById('organize_widget_script');
    parentNode = organizeScriptNode.parentNode;

    parentNode.insertBefore(organizeRegistrationBtnTag, organizeScriptNode);

})();
