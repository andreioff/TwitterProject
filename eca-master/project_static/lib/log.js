(function($, block) {
block.fn.log = function(config) {
    this.$element.addClass('block log').append($('<ul>').append('<li>'));
    this.actions(function(e, message){
        $ul = $('ul:first-child', this);
        $ul.find("> li:first-child").text(message.text);
        $(this).scrollTop(1);
    });
    return this.$element;
};
})(jQuery, block);
