/*

 Copyright (c) 2010 Rick Vause, Mike Buttery

 Permission is hereby granted, free of charge, to any person
 obtaining a copy of this software and associated documentation
 files (the "Software"), to deal in the Software without
 restriction, including without limitation the rights to use,
 copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the
 Software is furnished to do so, subject to the following
 conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 OTHER DEALINGS IN THE SOFTWARE.

 */

(function($) {

$.fn.rte = function(fonts, options) {
	return this.each(function() {
		
		var frame;
		
		options = $.extend({
		    handle: 'rte-editor',
		    editor: 'maineditor',
		    className: 'editor',
		    width: '500px',
		    height: '300px',
		    onAction: function() {
		        $(this).val(frame.document.body.innerHTML);
		    },
		}, options);
		
		var content = this;
		
		var editor_style = '<style>';
		var editor = 
			'<div class="'+ options.handle +'">' +
				'<ul class="rte-options">' +
					'<li class="rte-button rte-bold" id="go-bold"><a href="javascript:void(0);" title="Bold">Bold</a></li>' +
					'<li class="rte-button rte-italic" id="go-italic"><a href="javascript:void(0);" title="Italic">Italic</a></li>' +
					'<li class="rte-button rte-underline" id="go-underline"><a href="javascript:void(0);" title="Underline">Underline</a></li>';
		/*if (typeof fonts != 'undefined') {
			editor += '<li class="rte-select rte-font"><select id="go-font">' + 
					'<option value="Default">Font</option>';
			for (var i in fonts) {
				if (fonts.hasOwnProperty(i)) {
					editor += '<option class="font-' + i +'" value="' + fonts[i].name + '">' + fonts[i].name + '</option>';
					editor_style += '@font-face {\n' +
					                'font-family: \'' + fonts[i].name + '\';\n' + 
					                'src: url(\'' + fonts[i].msie + '\');\n' + 
					                'src: local(\'☺\'), url(\'' + fonts[i].src + '\') format(\'' + fonts[i].format + '\');\n' +
					                '}\n\n';
					editor_style += '.font-' + i + '{ font-family: "' + fonts[i].name + '"; font-size: 12pt; }\n\n';
				}
			}
			editor += '</select></li>';
		}*/
		if (typeof fonts != 'undefined') {
			editor += '<li class="rte-select rte-font"><ul id="go-font">' +
					'<li val="Default">Font</option>';
			for (var i in fonts) {
				if (fonts.hasOwnProperty(i)) {
					editor += '<li class="font-' + i + '" val="' + fonts[i].name + '">' + fonts[i].name + '</li>';
					editor_style += '@font-face {\n' +
									'font-family: \'' + fonts[i].name + '\';\n' +
									'src: url(\'' + fonts[i].msie + '\');\n' +
									'src: local(\'☺\'), url(\'' + fonts[i].src + '\') format(\'' + fonts[i].format + '\');\n' +
									'}\n\n';
					editor_style += '.font-' + i + '{ font family: "' + fonts[i].name + '"; font-size: 12pt; }\n\n';
				}
			}
			editor += '</ul></li>';
		}
		editor += '<li class="rte-select rte-size"><select id="go-size">' +
					'<option value="Default">Size</option>' +
					'<option value="1">8pt</option>' +
					'<option value="2">10pt</option>' +
					'<option value="3">12pt</option>' +
					'<option value="4">14pt</option>' +
					'<option value="5">18pt</option>' +
					'<option value="6">24pt</option>' +
					'<option value="7">36pt</option>' +
				'</select></li>';
		editor += '<li class="rte-select rte-justify"><select id="go-justify">' +
					'<option value="Default">Justify</option>' + 
					'<option value="Left">Left</option>' +
					'<option value="Center">Center</option>' +
					'<option value="Right">Right</option>' +
				'</select></li>';
		editor += '<li class="rte-button rte-shadow" id="go-shadow"><a href="javascript:void(0);">Shadow</a></li>';
		editor += '<li class="rte-button rte-undo" id="go-undo"><a href="javascript:void(0);">Undo</a></li>' +
					'<li class="rte-button rte-redo" id="go-redo"><a href="javascript:void(0);">Redo</a></li>';
		editor += '<li class="rte-button rte-removeformat" id="go-removeformat"><a href="javascript:void(0);">Remove Format</a></li>';
		editor += '</ul>' +
		        '</div>' + 
		        '<div class="frame">' +
				'<iframe name="' + options.editor + '" class="' + options.className + '" frameborder="0" style="width: ' + options.width + '; height: ' + options.height + ';"></iframe>' +
			'</div>';
		editor_style += '</style>';
			
		$(content).hide().before(editor_style).after(editor);
		
		$('ul#go-font').css3select({
			callback: function(val) {
				frame.document.execCommand('fontName', false, val);
				options.onAction.call(content);
			}
		});
		
		var frame = parent.frames[0];
		var frame_content = '<!DOCTYPE html><html><head>';
				
		frame_content += editor_style;
		frame_content += '<base href="' + $('base').attr('href') + '"></head><body>' + $(content).val() + '</body></html>';
		
		frame.document.open();
		frame.document.write(frame_content);
		frame.document.close();
		frame.document.contentEditable = 'true';
		frame.document.designMode = 'on';
		$(frame.document).focus();
		
		// Bold
		$('#go-bold').bind('click', function(e) {
			frame.document.execCommand('bold', false, null);
			options.onAction.call(content);
		});
		
		// Italic
		$('#go-italic').bind('click', function(e) {
			frame.document.execCommand('italic', false, null);
			options.onAction.call(content);
		});
		
		// Underline
		$('#go-underline').bind('click', function(e) {
			frame.document.execCommand('underline', false, null);
			options.onAction.call(content);
		});
		
		// Set Font
		/*$('#go-font').bind('change', function(e) {
			frame.document.execCommand('fontName', false, $(this).val());
			$(this).val('Default');
			options.onAction.call(content);
		});*/
		
		// Set Font Size
		$('#go-size').bind('change', function(e) {
			frame.document.execCommand('fontSize', false, $(this).val());
			$(this).val('Default');
			options.onAction.call(content);
		});
		
		// Align Text
		$('#go-justify').bind('change', function(e) {
			if ($(this).val() == 'Left')
				frame.document.execCommand('justifyLeft', false, null);
			else if ($(this).val() == 'Center')
				frame.document.execCommand('justifyCenter', false, null);
			else
				frame.document.execCommand('justifyRight', false, null);
			$(this).val('Default');
			options.onAction.call(content);
		});
		
		// Undo / Redo
		$('#go-undo').bind('click', function(e) {
			frame.document.execCommand('undo', false, null);
			options.onAction.call(content);
		});
		
		$('#go-redo').bind('click', function(e) {
			frame.document.execCommand('redo', false, null);
			options.onAction.call(content);
		});
		
		// Remove Formatting
		$('#go-removeformat').bind('click', function(e) {
			frame.document.execCommand('removeFormat', false, null);
			options.onAction.call(content);
		});
		
		// Add Shadow
		/*$('#go-shadow').bind('click', function(e) {
		    var text = '';
		    if (frame.document.getSelection)
		        text = frame.document.getSelection();
		    else if (frame.document.selection)
		        text = frame.document.selection.createRange().text;
		    frame.document.execCommand('insertHTML', false, '<span style="text-shadow: 2px 2px 2px #000;">' + text +'</span>');
		    options.onAction.call(content);
		});*/
		
		// Get Value
		$('#get-val').bind('click', function(e) {
			$(content).val(frame.document.body.innerHTML);
			console.log($(content).val());
		});
		
	});
}

})(jQuery);
