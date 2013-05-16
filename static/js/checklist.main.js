var GET_SIMPLE_CHECKLIST_ACTION = 'get_simple_checklist';
var GET_DELIMITED_ACTION = 'get_delimited';

Array.prototype.unique = function() {
    var a = this.concat();
    for(var i=0; i<a.length; ++i) {
        for(var j=i+1; j<a.length; ++j) {
            if(a[i] === a[j])
                a.splice(j, 1);
        }
    }

    return a;
};
String.prototype.endsWith = function (suffix) {
    return this.indexOf(suffix, this.length - suffix.length) !== -1;
};
jQuery.fn.outerHTML = function () {
    return jQuery('<div></div>').append(this.clone()).html();
};
function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search)||[,null])[1]
    );
}
function validateEmail(elementValue) {
    var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return emailPattern.test(elementValue);
}
function allSwiped(item) {
    return item.parent().children('li').length ==
        item.parent().children('.item-removed').length;
}
function addSwipe(item, parent) {
    item.bind('swipeleft', function (event, ui) {
        var items = [];
        if (localStorage.items_done != null) {
            items = $.parseJSON(localStorage.items_done);
        }
        items.push(item.attr('desk-item'));
        localStorage.items_done = JSON.stringify(items);
        item.find('a').addClass('item-removed');
        item.addClass('item-removed');
        if (parent != null && allSwiped(item))
            parent.trigger('swipeleft');
    });
    item.bind('swiperight', function (event, ui) {
        if (localStorage.items_done != null) {
            var items = $.parseJSON(localStorage.items_done);
            items.splice(items.indexOf(item.attr('desk-item')),1);
        }
        localStorage.items_done = JSON.stringify(items);
        item.find('a').removeClass('item-removed');
        item.removeClass('item-removed');
        if (parent != null)
            parent.trigger('swiperight');
    });
}
function addSwipeDelete(item, container) {
    item.bind('swipeleft', function (event, ui) {
        item.remove();
        container.listview('refresh');
        if (item.attr('offer_id') != null) {
            var offer_ids = $.parseJSON(localStorage.promoted);
            offer_ids.splice(offer_ids.indexOf(item.attr('offer_id')),1);
            localStorage.promoted = JSON.stringify(offer_ids);
        } else {
            var items = $.parseJSON(localStorage.checklist_json);
            items.splice(items.indexOf(item.attr('name')),1);
            localStorage.checklist_json = JSON.stringify(items);
        }
    });
}
function addSelect(item, button) {
    button.bind('vclick', function (event, ui) {
        if (button.find(':contains("Select Category")').length > 0) {
            button.find('span span').html('Deselect Category');
            button.parent().parent().parent().attr('item_selected', 'true');
            item.find('span.ui-icon').removeClass("ui-icon-arrow-r").addClass("ui-icon-check");
            item.attr('item_selected', 'true');
        } else {
            button.find('span span').html('Select Category');
            button.parent().parent().parent().removeAttr('item_selected');
            item.find('span.ui-icon').removeClass("ui-icon-check").addClass("ui-icon-arrow-r");
            item.removeAttr('item_selected');
        }
        $('#checklist-items').listview('refresh');
    });
}
function initIcon(item, iconBtn) {
    iconBtn.bind('vclick', function (event, ui) {
        if (item.attr('item_selected') == 'true') {
            iconBtn.removeClass("ui-icon-check").addClass("ui-icon-plus");
            item.removeAttr('item_selected');
        } else {
            iconBtn.removeClass("ui-icon-plus").addClass("ui-icon-check");
            item.attr('item_selected', 'true');
        }
        $('#checklist-items').listview('refresh');
    });
}
function initItem(item, parent) {
    var itemHTML = $('<li name=' + item.split(' ').join('_') + '>' + item + '</li>');
    itemHTML.addClass('item-2-large');
    addSwipeDelete(itemHTML, parent);
    return itemHTML;
}
function sortChecklist() {
    $('#checklist-items>li').tsort({order:'desc', attr:'num-children'});
}
function createCategorized() {
    $.each($.parseJSON(localStorage.checklist_json), function (item, categories) {
        $.each(categories, function () {
            if ($("#checklist-items li[name='" + this + "']").length == 0) {
                var ulItem = $("<li name='" + this + "' num-children='1' data-filtertext='" + this + " " + item + "'>" + this + "</li>");
                var selectBtn = $('<a href="checklist.html" data-rel="back" data-role="button" data-theme="a">Select Category</a>');
                var backBtn = $('<a href="checklist.html" data-rel="back" data-role="button">Back</a>');
                addSelect(ulItem, selectBtn);

                $("#checklist-items").append(ulItem);
                $("#checklist-items li[name='" + this + "']").append('<ul></ul>');
                $("#checklist-items li[name='" + this + "'] ul").append(initItem(item, ulItem));
                $("#checklist-items li[name='" + this + "'] ul").append(selectBtn);
                $("#checklist-items li[name='" + this + "'] ul").append(backBtn);
            } else if ($("#checklist-items li[name='" + this + "'] ul li[name='" + item + "']").length == 0) {
                var currItem = $("#checklist-items li[name='" + this + "']");
                currItem.attr('num-children', currItem.attr('num-children') + '1');
                currItem.attr('data-filtertext', currItem.attr('data-filtertext') + ' ' + item);
                $("#checklist-items li[name='" + this + "'] ul").prepend(initItem(item, currItem));

                var classDefNum = $("#checklist-items li[name='" + this + "'] ul li").length;
                if (classDefNum > 1) {
                    currItem.addClass(classDefNum > 3 ? 'item-4-large' : 'item-' + classDefNum + "-large");
                }
            }
        });
    });
    sortChecklist();
}
function createSimple() {
    $.each($.parseJSON(localStorage.checklist_json), function (i, item) {
        if ($("#checklist-items li[name='" + item.split(' ').join('_') + "']").length == 0) {
            var icon = $('<span class="ui-icon ui-icon-plus ui-icon-shadow"></span>');
            var liItem = initItem(item, $("#checklist-items"));

            liItem.addClass('ui-btn ui-btn-up-a ui-btn-icon-right ui-li-has-arrow');
            liItem.attr('data-iconpos', 'right');
            liItem.attr('data-icon', 'plus');
            liItem.append(icon);
            initIcon(liItem, icon);

            $("#checklist-items").append(liItem);
        }
    });
}
function createItems() {
    if (localStorage.promoted != null) {
        $('#checklist-items').append(localStorage.promoted);
        createPromoted('#checklist-items');
    }
    if (localStorage.checklist_json != null) {
        createSimple();
    }
    $('#checklist-items').listview('refresh');
}
function createPromoted(list_id) {
    $(list_id + ' li').each(function () {
        var icon = $('<span class="ui-icon ui-icon-plus ui-icon-shadow"></span>');
        $(this).addClass('ui-btn ui-btn-up-a ui-btn-icon-right ui-li-has-arrow');
        $(this).append(icon);
        initIcon($(this), icon);
        addSwipeDelete($(this), $(list_id));
    });
    $(list_id).listview('refresh');
}
function getPlainMessage(delimeter) {
    var messageBody = '';
    $.each($.parseJSON(localStorage.selected_items), function (index, value) {
        messageBody += value + delimeter;
        if ($('div[data-role="page"]').length > 1) {
            $.each($.parseJSON(localStorage.checklist_json), function (item, categories) {
                if (categories.indexOf(value) !== -1) {
                    messageBody += '--' + item + delimeter;
                }
            });
        }
    });
    return messageBody;
}
function getInvertedJSON() {
    if ($('div[data-role="page"]').length > 1) {
        var selected = $.parseJSON(localStorage.selected_items);
        var original = $.parseJSON(localStorage.checklist_json);
        var inverted = {};

        $.each(selected, function (index, value) {
            inverted[value] = [];
            $.each(original, function (item, categories) {
                if (categories.indexOf(value) !== -1) {
                    inverted[value].push(item);
                }
            });
        });

        return JSON.stringify(inverted);
    } else {
        return localStorage.selected_items;
    }
}
function collectSelectedItems() {
    var selected_items = [];
    var selected_offers = [];
    $('#checklist-items li[item_selected]').each(function () {
        if ($(this).attr('offer_id') != null) {
            selected_offers.push($(this).attr('offer_id'));
        } else {
            selected_items.push($(this).attr('name'));
        }
    });
    localStorage.selected_items = JSON.stringify(selected_items);
    localStorage.selected_offers = JSON.stringify(selected_offers);
}
function collectPromotedItems() {
    localStorage.promoted = '';
    $('#promoted-items li[item_selected]').each(function () {
        $(this).find('span').remove();
        $(this).removeClass('item-removed');
        $(this).removeAttr('item_selected');
        localStorage.promoted += $(this).outerHTML();
    });
}
function executeAndChangePage(action, button) {
    $.mobile.showPageLoadingMsg();
    button.addClass('ui-btn-active');
    var token = $('[name="csrfmiddlewaretoken"]').attr('value');
    $.post(action + '.html', {words:$('#words').val(), csrfmiddlewaretoken:token}, function (json) {
        if (localStorage.checklist_json != null) {
            var current_json = $.parseJSON(localStorage.checklist_json);
            json = current_json.concat(json).unique();
        }
        localStorage.checklist_json = JSON.stringify(json);
        $.mobile.changePage("checklist.html");
        button.removeClass('ui-btn-active');
    }, 'json');
}
function processSimple(button) {
    executeAndChangePage(GET_SIMPLE_CHECKLIST_ACTION, button);
}
function processDelimited(button) {
    executeAndChangePage(GET_DELIMITED_ACTION, button);
}
function bindIndexPage() {
    $(document).bind('pageload', function (event, data) {
        if (data.url.endsWith('login') && $('#login-errors').length == 0) {
            $.mobile.changePage('index.html', {reloadPage:true});
        }
    });
    $(document).bind('pageshow', function (event, data) {
        createItems();

        if (data.prevPage[0]) {
            var divId = data.prevPage[0].getAttribute('id');
            if (divId && divId != 'login-page') {
                var prevUrl = divId.replace('-page', '.html');
                $('#cancel-btn').attr('href', prevUrl);
            }
        }
        $("#recipient").change(function () {
            if (validateEmail($(this).val())) {
                $("#send_in_person").removeClass('ui-disabled');
            } else {
                $("#send_in_person").addClass('ui-disabled');
            }
        });
        $("#advanced-flip").change(function () {
            if ($(this).val() == 'on') {
                $("#simple").css('display', 'block');
            } else {
                $("#simple").css('display', 'none');
            }
        });
        $("#send-checklist").bind('vclick', function (event, ui) {
            collectSelectedItems();
            var checklist = $('div[item_selected]');

            if (checklist.length > 0) {
                checklist = $('<div></div>');
                $('div[item_selected]').each(function () {
                    var item = $(this).clone();
                    item.removeClass('ui-body-a');
                    item.removeClass('ui-page');
                    item.css('display', 'block');
                    item.css('min-height', '100px');
                    item.find('ul a').remove();
                    checklist.append(item);
                });
            } else {
                checklist = $('#checklist-items').clone();
                checklist.empty();

                $('#checklist-items li[item_selected]').each(function () {
                    checklist.append($(this).clone());
                });
            }

            localStorage.htmlToSend = '<html><head>' + $('head link').outerHTML() + '</head><body>' + checklist.outerHTML() + '</body></html>';
        });
        $("#send_in_person").bind('vclick', function (event, ui) {
            $("#send_in_person").attr("href", "mailto:" + $("#recipient").val() + "?subject=Your Smartest Checklist&body=" + getPlainMessage('%0A'));
            clearStorage();
        });
        $("#send_by_system").bind('vclick', function (event, ui) {
            var token = $('[name="csrfmiddlewaretoken"]').attr('value');
            if (validateEmail($('#recipient').val())) {
                $.post('send_checklist.html', {recipient:$('#recipient').val(), plain_text:getPlainMessage('\n'), plain_html:localStorage.htmlToSend, csrfmiddlewaretoken:token}, function (respond) {
                    alert(respond);
                    $.mobile.changePage('index.html');
                });
            } else {
                $.post('create_checklist.html', {recipient:$('#recipient').val(), checklist_json:getInvertedJSON(), offers_json:localStorage.selected_offers, csrfmiddlewaretoken:token}, function (respond) {
                    alert(respond);
                    $.mobile.changePage('index.html');
                });
            }
            clearStorage();
        });
        $('#select-all').bind('vclick', function (event, ui) {
            if ($('#select-all').find(':contains("Select All")').length > 0) {
                $('#select-all span span').html('Deselect All');
                $("#checklist-items li").each(function () {
                    $(this).attr('item_selected', 'true');
                });
                $("#checklist-items li span.ui-icon").each(function () {
                    $(this).removeClass("ui-icon-plus").addClass("ui-icon-check");
                });
            } else {
                $('#select-all span span').html('Select All');
                $("#checklist-items li").each(function () {
                    $(this).removeAttr('item_selected');
                });
                $("#checklist-items li span.ui-icon").each(function () {
                    $(this).removeClass("ui-icon-check").addClass("ui-icon-plus");
                });
            }
        });
        $.each($('[error-id]'), function () {
            var outer = $(this);
            var id = outer.attr('error-id');
            $('#' + id).css('border-color', 'red');
            $('#' + id).focus(function () {
                outer.show();
            });
            $('#' + id).blur(function () {
                outer.hide();
            });
        });

        $.mobile.hidePageLoadingMsg();
    });
}
function bindPersonalPage(page) {
    $(document).bind('pageshow', function (event, data) {
        $("#send-checklist").addClass('ui-disabled');
        $("#checklist-done").bind('vclick', function (event, ui) {
            localStorage.removeItem('items_done');
            if ($("#checklist-done").attr('href') == 'my_desk.html') {
                var token = $('[name="csrfmiddlewaretoken"]').attr('value');
                $.post('check_done.html', {checklist_id:getURLParameter('id'), csrfmiddlewaretoken:token});
            }
        });
        $("#checklist-done").attr('href', page);
        var items_done = $.parseJSON(localStorage.items_done);
        $.each($('[desk-item]'), function () {
            if (items_done != null && items_done.indexOf($(this).attr('desk-item')) > -1) {
                $(this).addClass('item-removed');
            }
            if ($(this).attr('parent-desk-item') != null) {
                addSwipe($(this), $('[desk-item="' + $(this).attr('parent-desk-item') + '"]'));
            } else {
                addSwipe($(this), null);
            }
        });
    });
}
function bindOffersPage() {
    $(document).bind('pageshow', function (event, data) {
        createPromoted('#promoted-items');
    });
}
function clearStorage() {
    localStorage.removeItem('promoted');
    localStorage.removeItem('htmlToSend');
    localStorage.removeItem('selected_items');
    localStorage.removeItem('selected_offers');
    localStorage.removeItem('checklist_json');
}
function initDefaults() {
    $.mobile.defaultPageTransition = "flip";
}
