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
		selector = 'input#' + uikey + ', select#' + uikey + ', textarea#'+uikey;
		if ($(selector).length != 0) {
			try {
				if ($(selector).prop('type') === 'checkbox') {
					$(selector).prop('checked',	model[key]);
				} else {
					$(selector).val(model[key]);
				}
			} catch (e) {
				console.log('couldn\'t set ' + prefix + '|' + key)
			}
		}
	}
}