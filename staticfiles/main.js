var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}

let sidemenu = document.querySelector(".ppo")
let navbar = document.querySelector(".sideMenu")
let closeMenu = document.querySelector(".closeSm")
let dropBtn = document.querySelector(".cki")
let dropContent = document.querySelector(".productMenu-content")
sidemenu.addEventListener('click', (e) => { 
	navbar.style.display = 'block'
})

closeMenu.addEventListener('click', (e) => { 
	navbar.style.display = 'none'
})

dropBtn.addEventListener('click', (e) => { 
	dropContent.style.display = 'block'
})

dropBtn.addEventListener('mouseleave', (e) => { 
	dropContent.style.display = 'none'
})

$(document).on('submit', '#form-product-create', (e) => {
    e.preventDefault();

    $.ajax({
        type: 'POST',
        url: '/createProduct',
        data: {
            name: $('#name').val(),
            label: $('#label').val(),
            price: $('#price').val(),
            image: $('#image').val(),
            category: $('#category').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: (data) => {
            $('h3').html(data)
        }

    })
})