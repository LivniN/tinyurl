function get_tiny_url() {
    base_url = document.getElementById("base_url").value;
    fetch('post_new_url', {
        method: "POST",
        credentials: "include",
        body: JSON.stringify({ 'base_url': base_url }),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then(function(data) {
        console.log(data)
    })

}


function copy_text() {
    /* Get the text field */
    var copyText = document.getElementById("tiny_url_output");

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/

    /* Copy the text inside the text field */
    document.execCommand("copy");
}