function loadOrganizeIframe() {
    var iframeTag = document.createElement('iframe');
    iframeTag.setAttribute('id', 'organize_iframe');
    iframeTag.setAttribute('src', 'https://register-dev.organize.org/?widget_id=' + organizeWidgetId);
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

(function() {
    var isMobile = false;
    // device detection
    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) || screen.width <= 480)
    {
        isMobile = true;
    }

    var linkTag = document.createElement('link');
    linkTag.setAttribute('rel', 'stylesheet');
    linkTag.setAttribute('href', '//d1qr8e9x47knhm.cloudfront.net/static/css/modal.css');
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
        if (organizeAlwaysOpenInPage == true) {
            organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: loadOrganizeIframe();');
        }
        else {
            organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: window.open(\'https://register-dev.organize.org/?widget_id=' + organizeWidgetId + '\');');
        }
    }
    else
    {
        organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: window.open(\'https://register-dev.organize.org/?widget_id=' + organizeWidgetId + '\');');
    }

    organizeRegistrationBtnTag.setAttribute('class', 'organize-registration-btn');
    organizeRegistrationBtnTag.setAttribute('id', 'organize_registration_btn');
    var widgetChoiceImagePath = "//d1qr8e9x47knhm.cloudfront.net/static/images/widget/" + organizeWidgetChoice + ".png";
    organizeRegistrationBtnTag.innerHTML = '<img style="height: 100%;border:1px solid #021a40;" src="' + widgetChoiceImagePath + '"/>';

    organizeScriptNode = document.getElementById('organize_widget_script');
    parentNode = organizeScriptNode.parentNode;

    parentNode.insertBefore(organizeRegistrationBtnTag, organizeScriptNode);

})();



