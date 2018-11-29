function updatePoints(direction) {
    let selectedRadio = $("input[name='corner-select']:checked").val();
    if (selectedRadio) {
        $.ajax({
            url: "setup/update_point",
            type: "POST",
            data: {direction: direction, point: selectedRadio},
            dataType: "json",
            success: function (result) {
                location.reload(true);
            }
        });
    }
}

function saveSettings() {
    $.ajax({
       url: "setup/save_settings",
       type: "POST",
       success: function (result) {
           alert("Saved settings!");
       }

    });
}