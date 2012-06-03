var Utils = {
	renderFieldErrorTooltip : function(selector, msg, placement) {
		var elem;
		if (typeof placement === 'undefined') {
			placement = 'right'; // default to right-aligned tooltip
		}
		elem = $(selector);
		elem.tooltip({
			'title' : msg,
			'trigger' : 'manual',
			'placement' : placement
		});
		elem.tooltip('show');
		elem.addClass('error');
		elem.on('focus click', function(e) {
			elem.removeClass('error');
			elem.tooltip('hide');
		});
	}
};

/* Your custom JavaScript here */

function initForm(model, prefix) {
	prefix = typeof prefix !== 'undefined' ? prefix : '';
	for (key in model) {
		uikey = prefix + '-' + key;
		if ($('input#' + uikey + ', select#' + uikey).length != 0) {
			try {
				if ($('input#' + uikey).attr('type') === 'checkbox') {
					$('input#' + uikey).attr('checked',
							model[key] === 'True' ? 'checked' : false);
				} else {
					$('input#' + uikey + ', select#' + uikey).val(model[key]);
				}
			} catch (e) {
				console.log('couldn\'t set ' + prefix + '|' + key)
			}
		}
	}
}