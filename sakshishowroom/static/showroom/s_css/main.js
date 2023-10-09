var menu_toggle = 1;

$(".menu-btn").click(function(e) {
    const menu_li = $(".menu-items ul li");
    menu_toggle += 1;
    
    if(menu_toggle%2==0){
        $('.menu-items').animate({height:'231px'},);
        for (let li of menu_li){
            $(li).show(500);
        }
    }else{
        for (let li of menu_li){
            $(li).hide('fast');
        }
        $('.menu-items').animate({height:'0px'},);

    }
});


function AddToCart(id, btn) {
    $.ajax({
        type: "POST",
        url:'../../showroom/cart/set',
        data:{
            'item': id,
        }, 
        success: function(data, status, xhr){
            $(btn).hide();
            $(btn).siblings().fadeIn("slow");

        },
        error: function(message) {
            $(btn).text("Error Occured");
            
        },
    });

}

function RemoveFromCart(id, btn){
    $.ajax({
        type: "POST",
        url:'../../showroom/cart/delete',
        data:{
            'item': id,
        }, 
        success: function(data, status, xhr){
            $(btn).hide();
            $(btn).siblings().fadeIn("slow");
        },
        error: function(){
            $(btn).text("Error Occured");
        }
    });
}

function Decrease(id, btn ){
    let prev_qtty = UserCart[id];

    prev_qtty -= 1;    
    if(prev_qtty <= 0){
        delete UserCart[id];
        $(btn).parent().parent().hide();
        $(btn).parent().parent().siblings().show();
    }else{
        UserCart[id] = prev_qtty;
    }
    $($(btn).siblings()[0]).text(UserCart[id]);
    localStorage.setItem('cart', JSON.stringify(UserCart));
    
}


$("#rzp-button1").click(function(){
    const phone = $("#cart_phone");
    const address = $("#cart_address");
    const username = $("#username").val();
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if(phone.val() == "" || address.val() == ""){
        $("#comm_form_err").show();
        phone.addClass("border-rose-600");
        address.addClass("border-rose-600");
    }else{
        $.ajax({
            url: "#",
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            method:"POST",
            dataType:"json",
            username: username,
            data: {
                "phone": phone.val(),
                "address": address.val(),
            },
            success: function(data){
                var options = {
                        "key":data.keyid, // Enter the Key ID generated from the Dashboard
                        "amount": data.razor_pay_order.amount, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Sakshi Showroom", //your business name
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        "order_id": data.razor_pay_order.id , //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (response){
                            $.ajax({
                                url: "../payment/verify",
                                headers: {'X-CSRFToken': csrftoken},
                                mode: 'same-origin',
                                method:"POST",
                                username: username,
                                data: {
                                    "razorpay_payment_id":response.razorpay_payment_id,
                                    "razorpay_order_id":response.razorpay_order_id,
                                    "razorpay_signature":response.razorpay_signature,
                                },
                                success: function (data){
                                    console.log(data);
                                    if(data.status == "success"){
                                        alert("Order created successfully");
                                        window.location.href = "../../showroom?cart=clear";
                                    }else{
                                        alert("Order not created successfully");
                                    }
                                },
                            });
                        },
                        "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information especially their phone number
                            "name": data.user, //your customer's name
                            "email": "gaurav.kumar@example.com",
                            "contact":data.phone,  //Provide the customer's phone number for better conversion rates 
                        },
                        "notes": {
                            "address":data.address
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };

                var rzp1 = new Razorpay(options);
                rzp1.open();

            },
            error: function(jqXHR, textStatus, errorThrown){
                console.log(textStatus);
            },
        });
    }


});

const orderBox = document.querySelectorAll("#orderBox");
orderBox.forEach(function(box){
    $(box).click(function(){
        const i = $(box).children('div.hidden_sub_box');
        $(i).toggle((i) => $(i).show(), (i) => $(i).hide());
    });
});

// function orderBoxExpand(){
//     const orderBox = $("#orderBox");
//     const i = document.querySelector("#orderBox i");
//     const b = document.querySelector("#orderBox div.hidden_sub_box");
//     $(b).show();
// }