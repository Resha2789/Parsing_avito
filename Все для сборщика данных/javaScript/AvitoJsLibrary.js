

function count_all_items(){
    var el = $("[data-marker='page-title/count']");
    if (el.length == 0) {
        return false;
    }

    return Number(el.text())
}

function count_items_in_page(){
    var el = $("[data-marker='item']");
    if (el.length == 0) {
        return false;
    }

    return el.length
}

function get_title_and_url_items(){
    var el = $("[data-marker='item']");
    if (el.length == 0) {
        return false;
    }

    var titles = [];
    var url = [];

    for (var i = 0; i < el.length; i++) {
        if ($("[data-marker='item']").eq(i).find("span:contains('Показать телефон')").length > 0){
            titles.push(el.eq(i).find("[itemprop='name']").text());
            url.push('https://www.avito.ru/' + el.eq(i).find("[itemprop='url']").eq(1).attr("href"));
        }
    }

    return [titles, url];
}


function url_item(index) {
    var el = $("[data-marker='item']").eq(index).find("[itemprop='url']").eq(1);
    if (el.length == 0) {
        return false;
    }

    return 'https://www.avito.ru/' + el.attr('href');
}

function url_open(url) {
   window.open(url, 'New TAB');
   return true;
}

function click_phone() {
    var el = $("span:contains('XXX-XX-XX')");
    var el2 = $("span:contains('Без звонков')");
    if (el.length == 0) {
        if (el2.length > 0){
            return "Без звонков";
        }
        return false;
    }
    el.focus();
    el.click();

    return true;
}
function set_id_for_phone() {
    var el = $("[src^='data:image/png;base64']").eq(2);
    if (el.length == 0) {
        return false;
    }
    el.attr('id', 'phone_number');


    return true;
}

function name(){
    var el = $("[data-marker='seller-info/name']").eq(0);
    if (el.length == 0) {
        return false;
    }

    var str = el.text();
    var name = "";
    if (str.match(/[^\s]+/)){
        name = str.replace(/(\n+)|(\s+)/g, "");
    }
    return name;
}

function last_page(){
    var el = $("[data-marker^='page(']");
    if (el.length == 0) {
        return false;
    }
    last_page = $("[data-marker^='page(']").last().attr('data-marker');
    last_page = Number(last_page.match(/\d+/)[0]);

    return last_page;
}

function next_page(page){
    var el = $("[data-marker='page("+ page +")']");
    if (el.length == 0) {
        return false;
    }

    el.click();

    return true;
}

