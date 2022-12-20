    // $("#submit").click(function () {
    //     var text = $("#textarea").val();
    //     $("#modal_body").html(text);
    // });

    $(document).ready(function(){
        //addInvoiceDetail();

        if( $('#card_fcs').length )  //Check if element exist in page
        {
            $('html, body').animate({
                scrollTop: $('#card_fcs').offset().top
            }, 'slow');
        }

        //Product

        $("#id_is_discount").on('change', function(e) {
            e.preventDefault();
            if ($('#id_is_discount').is(':checked')){
                $('#discount_div').attr('hidden',false);
            }else{
                $('#id_discountPorcentage').val(0);
                $('#discount_div').attr('hidden',true);
            }
            

        })

        //Invoice
        $('.select-2-billing-customer').select2();
        //$('.select-2-shipping-customer').select2();

        $(".select-2-billing-customer").on('change', function(e) {
            e.preventDefault();
            var id_customer = $(this).val();
            $('#cust_names').text('');
            $('#cust_doc_num').text('');
            $('#cust_email').text('');
            $('#cust_phone').text('');
            $('#cust_address').text('');
            $('#cust_city').text('');

            getFillCustomerData(id_customer);
            

        })

        //Final Customer checkbox
        $("#id_is_final_customer").on('change', function(e) {
            e.preventDefault();
            if ($('#id_is_final_customer').is(':checked')){
                $('#id_billing_customer_id').attr('disabled',true);
            }else{
                $('#id_billing_customer_id').attr('disabled',false);
            }
            

        })

        //category product page
        $('.select-2-product-category').select2();

        $("#btn-add-category").click(function(e){
            e.preventDefault();
            var url = "addCategory";
            var cat_desc = $('#cat_desc_id').val();

            $.ajax({
                type: 'POST',
                url: url,
                data: {"cat_desc": cat_desc},
                success: function (response) {
                    if(response){
                        // Fetch the preselected item, and add to the control
                        var categSelect = $('.select-2-product-category');
                        $.ajax({
                            type: 'GET',
                            url: 'getCategoryById/' + response
                        }).then(function (data) {
                            // create the option and append to Select2
                            var option = new Option(data['description'], data['id'], true, true);
                            categSelect.append(option).trigger('change');

                            // manually trigger the `select2:select` event
                            categSelect.trigger({
                                type: 'select2:select',
                                params: {
                                    data: data
                                }
                            });
                        });
                        $('#modalAddCategory').modal('hide')               
                    }
                },
                error: function (response){ 
                    console.log(response)
                }
            });
        });
        


        //calls modal image product / set img src
        $(".modal_img").click(function(){
            $("#modalImg").modal('show');
            var img_field = document.getElementById("img_space");
            data_table = search_table_row_values("table_img",this);

            src_path = data_table[0];

            img_field.setAttribute("src", src_path);
        });


        //Modal Detalle Factura
        $(".modal_det_inv").click(function(){
            invoice_id = $('#id_invoice_glob').text()
            $("#modalDetInv").modal('show');
            data_table = search_table_row_values("invoiceDetailTable",this);
            $('#cod_prod_det_modal').text(data_table[0]);
            $('#id_quantity_det_modal').val(data_table[1]);
            $('#input_cod_prod_det_modal').val(data_table[0]);
        });

        $(".delete_det_inv").click(function(){
            invoice_id = $('#id_invoice_glob').text()
            data_table = search_table_row_values("invoiceDetailTable",this);
            var url = "delete/ajax/invoice/details/";

            $.ajax({
            type: 'GET',
            url: url,
            data: {"id_prod": data_table[0],
                    "id_invoice": invoice_id},
            success: function (response) {
                if(response){
                    setInterval('location.reload()', 1000);                    
                }
            },
            error: function (response){
                console.log(response)
            }
        })
            
        });

        
        $("#id_product_code").on('change', function(e) {
            e.preventDefault();
            this.blur();
            document.getElementById("form1").submit();
            
        })

        Dropzone.options.myGreatDropzone = { // camelized version of the `id`
            paramName: "file", // The name that will be used to transfer the file
            maxFilesize: 2, // MB
            accept: function(file, done) {
              if (file.name == "justinbieber.jpg") {
                done("Naha, you don't.");
              }
              else { done(); }
            }
          };

          
        //   $("#docNumbClie").on('change', function(e) {
        //     e.preventDefault();
        //     var numb_doc = $(this).val();
        //     var doc_type= $("#docTypeClie option:selected").text();

        //     if(doc_type == 'RUC'){
        //         getCustomerDataSRI(numb_doc);
        //     }else{
        //         console.log('no es Ruc');
        //     }
                

        //     $('#id_first_name').val('');
        //     $('#id_last_name').val('');
        //     $('#id_email').val('');
        //     $('#id_phone_1').val('');
        //     $('#id_phone_2').val('');
        //     $('#id_address').val('');
        //     $('#id_note').val('');

        // })

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

    function getFillCustomerData(id_customer){
        // GET AJAX request

        $.ajax({
            type: 'GET',
            url: "get/ajax/validate/customer/",
            data: {"id_customer": id_customer},
            success: function (response) {
                if(response){
                    $('#cust_names').text(response['customer_full_name']);
                    $('#cust_doc_num').text(response['customer_doc_num']);
                    $('#cust_email').text(response['customer_email']);
                    $('#cust_phone').text(response['customer_phone1']);
                    $('#cust_address').text(response['customer_address']);
                    $('#cust_city').text(response['customer_city']);                    
                }
            },
            error: function (response){
                console.log(response)
            }
        })
    }

    // function getCustomerDataSRI(numb_doc){
    //     // GET AJAX request

    //     $.ajax({
    //         type: 'GET',
    //         url: "get/ajax/validate/customerSri/",
    //         data: {"num_doc": numb_doc},
    //         success: function (response) {
    //             if(response){
    //                 $('#cust_names').text(response['customer_full_name']);
    //                 $('#cust_doc_num').text(response['customer_doc_num']);
    //                 $('#cust_email').text(response['customer_email']);
    //                 $('#cust_phone').text(response['customer_phone1']);
    //                 $('#cust_address').text(response['customer_address']);
    //                 $('#cust_city').text(response['customer_city']);                    
    //             }
    //         },
    //         error: function (response){
    //             console.log(response)
    //         }
    //     })
    // }


    // function updateInvoiceDetailModal(id_prod,id_invoice,prod_quantity){
    //     // GET AJAX request
    //     //var url = "newInvoice/" + id_invoice + "/update/ajax/invoice/details/";
    //     var url = "update/ajax/invoice/details/";
    //     $.ajax({
    //         type: 'PUT',
    //         url: url,
    //         data: {"id_prod": id_prod,
    //                 "id_invoice": id_invoice,
    //                 "prod_quantity": prod_quantity},
    //         success: function (response) {
    //             if(response){
    //                 console.log(response)                   
    //             }
    //         },
    //         error: function (response){
    //             console.log(response)
    //         }
    //     })
    // }
