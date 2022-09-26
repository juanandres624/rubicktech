    // $("#submit").click(function () {
    //     var text = $("#textarea").val();
    //     $("#modal_body").html(text);
    // });

    $(document).ready(function(){

        //calls modal image product / set img src

        $(".modal_img").click(function(){
            $("#modalImg").modal('show');
            var img_field = document.getElementById("img_space");
            data_table = search_table_row_values("table_img",this);

            src_path = data_table[0];

            img_field.setAttribute("src", src_path);
        });

    });

    function search_table_row_values(table_name,row_index) {
        var data = [];
        var table = document.getElementById(table_name);
        var ri = row_index.parentNode.parentNode.rowIndex;

        for (var i = 0; i < table.rows[ri].cells.length; i++) {
            data.push(table.rows[ri].cells.item(i).innerHTML);
        }

        return data;

        //getRowValue = table.rows[i].cells.item(0).innerHTML;

    }
