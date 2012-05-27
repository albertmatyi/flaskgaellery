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
		if (typeof fonts != 'undefined') {
			editor += '<li class="rte-select rte-font"><ul id="go-font">' +
					'<li val="Default" class="Default">Font</option>';
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
		editor += '<li class="rte-select rte-size"><ul id="go-size" name="size">' +
		          '<li val="3">Size</li>' + 
		          '<li val="1">8pt</li>' +
		          '<li val="2">10pt</li>' +
		          '<li val="3">12pt</li>' +
		          '<li val="4">14pt</li>' +
		          '<li val="5">18pt</li>' +
		          '<li val="6">24pt</li>' +
		          '<li val="7">36pt</li>' +
		          '</ul></li>';
		editor += '<li class="rte-button rte-left" id="go-left"><a href="javascript:void(0);">Left</a></li>';
		editor += '<li class="rte-button rte-center" id="go-center"><a href="javascript:void(0);">Center</a></li>';
		editor += '<li class="rte-button rte-right" id="go-right"><a href="javascript:void(0);">Right</a></li>';
		editor += '<li class="rte-button rte-color" id="go-color"><a href="javascript:void(0);">Color</a></li>';
		editor += '<li class="rte-button rte-undo" id="go-undo"><a href="javascript:void(0);">Undo</a></li>' +
					'<li class="rte-button rte-redo" id="go-redo"><a href="javascript:void(0);">Redo</a></li>';
		editor += '<li class="rte-button rte-removeformat" id="go-removeformat"><a href="javascript:void(0);">Remove Format</a></li>';
		editor += '</ul>' +
		        '</div>' + 
		        '<div class="frame">' +
				'<iframe name="' + options.editor + '" class="' + options.className + '" frameborder="0" style="width: ' + options.width + '; height: ' + options.height + ';"></iframe>' +
			'</div>';
		editor_style += '</style>';
		
		if (options.hideMenu) {
			 editor = '<div class="frame">' +
					  '<iframe name="' + options.editor + '" class="' + options.className + '" frameborder="0" style="width: ' + options.width + '; height: ' + options.height + ';"></iframe>' +
					  '</div>';
		}
					  			
		$(content).hide().before(editor_style).after(editor);
		
		// Font Select
		$('ul#go-font').css3select({
			callback: function(val) {
				frame.document.execCommand('fontName', false, val);
				options.onAction.call(content);
			}
		});
		
		// Size Select		
		$('ul#go-size').css3select({
			selectClassName: 'sizeselecter',
			optionClassName: 'sizeoptions',
		    callback: function(val) {
		        frame.document.execCommand('fontSize', false, val);
		        options.onAction.call(content);
		    }
		});
		
		// Color Select
		// This depends on the brilliant color picker plugin found here: http://www.mlambir.com.ar/project/show/mlcolorpicker		
		$('li#go-color').mlColorPicker({
			onChange: function(val) {
				frame.document.execCommand('foreColor',false, '#' + val);
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
		
		// Align Left		
		$('#go-left').bind('click', function(e) {
		    frame.document.execCommand('justifyLeft', false, null);
		    options.onAction.call(content);
		});
		
		// Align Center
		$('#go-center').bind('click', function(e) {
		    frame.document.execCommand('justifyCenter', false, null);
		    options.onAction.call(content);
		});
		
		// Align Right
		$('#go-right').bind('click', function(e) {
		    frame.document.execCommand('justifyRight', false, null);
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
		
		// Get Value
		$('#get-val').bind('click', function(e) {
			$(content).val(frame.document.body.innerHTML);
			console.log($(content).val());
		});
		
	});
}

})(jQuery);
