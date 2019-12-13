$(document).ready(function(){
    //############################# contact form functionality ##############################
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")

    contactForm.submit(function(event){
      event.preventDefault()
      
      var thisForm = $(this)
      //get form data
      var contactFormData = contactForm.serialize()


      $.ajax({
        url:contactFormEndpoint,
        method: contactFormMethod,
        data: contactFormData, 
        success: function(data){
          contactForm[0].reset()

          $.alert({
            title: "Message sent",
            content:data.message,
            theme: "modern"
          })
        },
        error: function(error){
          // get all error data array
          var jsonData = error.responseJSON
          var msg = ""

          // iterate to get each error
          $.each(jsonData,function(key,value){
            //msg += key + value[0].message + "<br/>"
            msg += value[0].message + "<br/>"
          })



          $.alert({
            title: "Ooops!",
            content: msg,
            theme: "modern"
          })
        }
      })
    })


    //############################# AutoSearch functionality ##############################
    var searchForm = $(".search-form")
    var searchInput = searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval = 1500
    var searchBtn = searchForm.find("[type='submit']")

    searchInput.keyup(function(event){
      //key released
      clearTimeout(typingTimer)
      typingTimer = setTimeout(performSearch,typingInterval)
      console.log("yeeep")
    })

    searchInput.keydown(function(event){
      //key pressed
      clearTimeout(typingTimer)
    })

    function displaySearching(){
      searchBtn.addClass("disabled")
      searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching... ")
    }

    function performSearch(){
      displaySearching()
      var query = searchInput.val()
      setTimeout(function(){
        window.location.href='/search/?q=' + query
      }, 1000)
      
    }

    //############################# Cart and add product functionality ##############################
    var productForm = $(".form-product-ajax")

    productForm.submit(function(event){
      event.preventDefault();

      var thisForm = $(this) 
      //var actionEndpoint = thisForm.attr("action");
      var actionEndpoint = thisForm.attr("data-endpoint"); // better for API endpoint
      var httpMethod = thisForm.attr("method");
      var formData = thisForm.serialize();

      $.ajax({
        url: actionEndpoint,
        method: httpMethod,
        data: formData,
        success: function(data){
          var submitSpan = thisForm.find(".submit-span")
          if (data.added) {
            submitSpan.html("In cart <button type='submit' class='btn btn-link'>Remove?</button>")
          } else {
            submitSpan.html("<button type='submit' class='btn btn-success'>Add to cart</button>")
          }

          //update cart items count
          var navbarCount = $(".navbar-cart-count")
          navbarCount.text(data.cartItemCount)

          //
          var currentPath = window.location.href
          if (currentPath.indexOf("cart") != -1 ) {
            refreshCart()
          }

        },
        error: function(errorData){
          $.alert({
            title: "Ooops!",
            content:"An error occurred",
            theme: "modern"
          })
        }
      }) // end of productForm.submit

      function refreshCart(){
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        var productRows = cartBody.find(".cart-products")
        var currentUrl = window.location.href

        var refreshCartUrl = '/api/cart'
        var refreshCartMethod = "GET"
        var data = {}
        $.ajax({
          url: refreshCartUrl,
          method: refreshCartMethod,
          data: data,
          success: function(data){
            var hiddenCartItemRemoveFrom = $(".cart-item-remove-form")

            if (data.products.length > 0){
              productRows.html(" ")

              $.each(data.products,function(index,value){
                //hiddenCartItemRemoveFrom.css("display", "none")

                var newCartItemRemove = hiddenCartItemRemoveFrom
                newCartItemRemove.css("display","block")
                newCartItemRemove.find(".cart-item-product-id").val(value.id)

                i = data.products.length
                cartBody.prepend("<tr><th scope=\"row\">" + i + "</th><td><a href=" + value.url + " '> " +
                  value.name + "</a>" + newCartItemRemove.html() + "</td><td>" + value.price + "</td></tr>")
                  hiddenCartItemRemoveFrom.css("display", "none")
                  i--
              })
              cartBody.find(".cart-subtotal").text(data.subtotal)
              cartBody.find(".cart-total").text(data.total)
            } else {
              window.location.href = currentUrl
            }
          },
          error: function(errorData){
            $.alert({
              title: "Ooops!",
              content:"An error occurred",
              theme: "modern"
            })
          }
        })
      } // end of function updateCart






    })

     




  })
