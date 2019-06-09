/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function (config) {
	// Define changes to default configuration here. For example:
	config.language = 'vi';
	//config.uiColor = '#008644';
    
    // config.toolbar = [
    //     { name: 'clipboard', groups: ['clipboard', 'undo'], items: ['Cut', 'Copy', 'Paste', '-', 'Undo', 'Redo'] },
    //     { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline'] },
    //     { name: 'paragraph', groups: ['list', 'indent', 'align'], items: ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'] },
    //     { name: 'insert', items: ['Image', 'Table'] },
    //     { name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize', '-', 'TextColor', 'BGColor', '-', 'Maximize'] }

    // ];
    config.resize_enabled = false;
    config.filebrowserBrowseUrl = '/File/Browser';
    config.filebrowserUploadUrl = '/File/Upload';
    config.dialog_noConfirmCancel = true;
};
