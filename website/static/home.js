var spinner = $('.overlay');
function show() {
    spinner.show();
    var source = new EventSource("/progress");
    source.onmessage = function (event) {
        if (event.data == 100) {
            spinner.hide();
            window.location.reload();
            source.close();
        }
        setTimeout(source, 1600);
    };
};
