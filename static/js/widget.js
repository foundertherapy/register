function loadOrganizeIframe() {
    var iframeTag = document.createElement('iframe');
    iframeTag.setAttribute('id', 'organize_iframe');
    iframeTag.setAttribute('src', organizeIFrameSRC);
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

    var linkTag = document.createElement('link');
    linkTag.setAttribute('rel', 'stylesheet');
    linkTag.setAttribute('href', organizeStyleSRC);
    linkTag.setAttribute('type', 'text/css');
    document.getElementsByTagName('head')[0].appendChild(linkTag);


    var organizeModalDivTag = document.createElement('div');
    organizeModalDivTag.setAttribute('id', 'organize_modal');
    organizeModalDivTag.setAttribute('class', 'organize-modal');


    var organizeModalContentDivTag = document.createElement('div');
    organizeModalContentDivTag.setAttribute('class', 'organize-modal-content');
    organizeModalContentDivTag.setAttribute('id', 'organize_modal_content');

    var organizeModalCloseDivTag = document.createElement('div');
    organizeModalCloseDivTag.setAttribute('onclick', 'javascript: closeOrganizeIframe()');
    organizeModalCloseDivTag.setAttribute('class', 'organize-close');
    organizeModalCloseDivTag.innerHTML = 'X';

    organizeModalContentDivTag.appendChild(organizeModalCloseDivTag);
    organizeModalDivTag.appendChild(organizeModalContentDivTag);

    document.getElementsByTagName('body')[0].appendChild(organizeModalDivTag);

    var organizeRegistrationDivTag = document.createElement('div');
    organizeRegistrationDivTag.setAttribute('id', 'organize_registration_div');
    organizeRegistrationDivTag.setAttribute('class', 'organize-registration-div');

    var organizeRegistrationBtnTag = document.createElement('div');
    organizeRegistrationBtnTag.setAttribute('onclick', 'javascript: loadOrganizeIframe();');
    organizeRegistrationBtnTag.setAttribute('class', 'organize-registration-btn');
    organizeRegistrationBtnTag.setAttribute('id', 'organize_registration_btn');
    organizeRegistrationBtnTag.innerHTML = 'Donate Now';

    organizeRegistrationDivTag.appendChild(organizeRegistrationBtnTag);

    organizeScriptNode = document.getElementById('organize_widget_script');
    parentNode = organizeScriptNode.parentNode;

    parentNode.insertBefore(organizeRegistrationDivTag, organizeScriptNode);

})();



