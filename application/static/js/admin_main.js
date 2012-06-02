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

function editElement(id, model) {
	for (key in model[id]) {
		if ($('input#' + key).length != 0) {
			try {
				if ($('input#' + key).attr('type') === 'checkbox') {
					$('input#' + key).attr('checked',
							model[id][key] === 'True' ? 'checked' : false);
				} else {
					$('input#' + key).val(model[id][key]);
				}
			} catch (e) {
				console.log('couldn\'t set ' + key)
			}
		}
	}
}

function resetForm() {
	formId = '';
	$(formId + ' input').each(function(idx, el) {
		if ($(el).attr('id') != 'csrf_token' && $(el).attr('type') != 'submit') {
			if ($(el).attr('type') == 'checkbox') {
				$(el).attr('checked', false);
			} else {
				$(el).val(undefined);
			}
		}
	});
}
