const API_BASE = "http://localhost:8000";


let state = {
    token: null,
    user: null,
    page: 1,
    limit: 8
};


async function api(path, options = {}) {


    let headers = options.headers || {};


    if (state.token) {

        headers["Authorization"] =
            "Bearer " + state.token;

    }


    const response = await fetch(
        API_BASE + path,
        {
            ...options,
            headers
        }
    );


    let data = null;


    try {
        data = await response.json();
    } catch {
    }


    if (!response.ok) {

        throw new Error(
            data?.detail || "Ошибка сервера"
        );

    }


    return data;

}


function showMessage(id, text, ok = false) {

    const el =
        document.getElementById(id);


    if (!el)
        return;


    el.innerText = text;


    el.className =
        ok ? "ok" : "error";

}


// ==========================
// NAVIGATION
// ==========================


document
    .querySelectorAll("nav button")
    .forEach(btn => {


        btn.onclick = () => {


            openView(
                btn.dataset.view
            );


        };


    });


function openView(name) {


    document
        .querySelectorAll(".view")
        .forEach(v => {

            v.classList.remove("active");

        });


    const view =
        document.getElementById(
            "view-" + name
        );


    if (view) {

        view.classList.add("active");

    }


    if (name === "catalog")
        loadProducts();


    if (name === "cart")
        loadCart();


    if (name === "orders")
        loadOrders();

    if (name === "seller")
        loadSellerProducts();

}


// ==========================
// REGISTER / LOGIN
// ==========================


let register = false;


document
    .getElementById("switchAuth")
    .onclick = () => {


    register = !register;


    document
        .getElementById("loginForm")
        .style.display =
        register ? "none" : "block";


    document
        .getElementById("registerForm")
        .style.display =
        register ? "block" : "none";


};


document
    .getElementById("loginForm")
    .addEventListener(
        "submit",
        async e => {


            e.preventDefault();


            const form =
                new FormData(e.target);


            const body =
                new URLSearchParams();


            body.append(
                "username",
                form.get("username")
            );


            body.append(
                "password",
                form.get("password")
            );

            try {


                const data =
                    await api(
                        "/auth/login",
                        {

                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/x-www-form-urlencoded"
                            },

                            body

                        }
                    );


                state.token =
                    data.access_token;


                await loadMe();
openView("catalog");

                toast(
    "Вы успешно вошли",
    "success"
);


            } catch (err) {

                toast(
                    err.message,
                        "error"
                    );

                }


        });


document
    .getElementById("registerForm")
    .addEventListener(
        "submit",
        async e => {


            e.preventDefault();


            const form =
                new FormData(e.target);


            const role =
                form.get("role");


            const url =
                role === "seller"
                    ?
                    "/auth/register-seller"
                    :
                    "/auth/register";


            try {


                await api(
                    url,
                    {

                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            username:
                                form.get("username"),

                            email:
                                form.get("email"),

                            password:
                                form.get("password")

                        })

                    }
                );


                showMessage(
                    "authMsg",
                    "Аккаунт создан. Проверьте Gmail и подтвердите email.",
                    true
                );


            } catch (err) {

                showMessage(
                    "authMsg",
                    err.message
                );

            }


        });


// ==========================
// USER
// ==========================


async function loadMe() {


    const user =
        await api("/auth/me");


    state.user = user;


    document
        .getElementById("userBox")
        .innerHTML =
        `
${user.username}
(${user.role})

<button id="logout">
Выйти
</button>
`;


    document
        .getElementById("logout")
        .onclick = logout;


    if (
        user.role === "seller"
        ||
        user.role === "admin"
    ) {

        document
            .getElementById("sellerTab")
            .style.display = "inline-block";

    }


}


function logout() {

    state.token = null;

    state.user = null;


    document
        .getElementById("userBox")
        .innerText = "Гость";


    openView("auth");

}


// ==========================
// PRODUCTS
// ==========================


async function loadProducts() {


    try {


        let params =
            new URLSearchParams();


        params.append(
            "page",
            state.page
        );


        params.append(
            "limit",
            state.limit
        );


        const search =
            document
                .getElementById("searchInput")
                .value;


        const sort =
            document
                .getElementById("sortSelect")
                .value;


        if (search)
            params.append(
                "search",
                search
            );


        if (sort)
            params.append(
                "sort",
                sort
            );


        const data =
            await api(
                "/products/?" +
                params.toString()
            );


        const products =
            data.items || data;


        const grid =
            document.getElementById(
                "productGrid"
            );


        grid.innerHTML = "";


        products.forEach(p => {


            grid.innerHTML +=
                `

<div class="product">


${p.image_url ?
                    `
<img src="${p.image_url}"
width="200">
`
                    :
                    ""}



<h3>
${p.name}
</h3>


<p>
${p.description || ""}
</p>


<b>
${p.price} ֏
</b>


<p>
Осталось:
${p.stock}
</p>



<button onclick="addToCart(${p.id})">

В корзину

</button>


</div>

`;


        });


    } catch (err) {

        showMessage(
            "catalogMsg",
            err.message
        );


    }


}


document
    .getElementById("searchBtn")
    .onclick = () => {

    state.page = 1;

    loadProducts();

};


// ==========================
// CREATE PRODUCT
// ==========================


document
    .getElementById("createProductBtn")
    .onclick = createProduct;


async function createProduct() {

    try {

        const product = await api(
            "/products/",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    name: sellerName.value,

                    description: sellerDescription.value,

                    price: Number(sellerPrice.value),

                    stock: Number(sellerStock.value)

                })

            }
        );


        const file =
            document.getElementById("sellerImage").files[0];


        if (file) {

            const formData = new FormData();

            formData.append(
                "file",
                file
            );

            await api(
                `/products/${product.id}/image`,
                {
                    method: "POST",
                    body: formData
                }
            );

        }

toast(
    "Товар добавлен",
    "success"
);


        loadProducts();

    }
    catch (err) {

        showMessage(
            "sellerMsg",
            err.message
        );

    }

}

async function loadSellerProducts(){


    try{


        const products =
            await api("/products/my");


        const box =
            document.getElementById(
                "sellerProducts"
            );


        box.innerHTML="";


        products.forEach(p=>{


            box.innerHTML +=
            `

            <div class="product">


            ${p.image_url ?
            `<img src="${p.image_url}" width="150">`
            :
            ""}


            <h3>
            ${p.name}
            </h3>


            <p>
            Цена:
            ${p.price} ֏
            </p>


            <p>
            Осталось:
            ${p.stock}
            </p>


            <button onclick="deleteProduct(${p.id})">

            Удалить

            </button>


            </div>


            `;


        });


    }
    catch(err){


        showMessage(
            "sellerMsg",
            err.message
        );


    }


}
async function deleteProduct(id){


    try{


        await api(
            "/products/"+id,
            {
                method:"DELETE"
            }
        );


        alert(
            "Товар удалён"
        );


        loadSellerProducts();


        loadProducts();


    }
    catch(err){

        alert(
            err.message
        );

    }


}
// ==========================
// CART
// ==========================


async function addToCart(id) {


    await api(
        "/cart/items",
        {

            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                product_id: id,

                quantity: 1

            })

        }
    );


    alert("Добавлено");

}


async function loadCart() {


    const cart =
        await api("/cart");


    const box =
        document.getElementById("cartBox");


    box.innerHTML = "";


    cart.items.forEach(item => {


        box.innerHTML +=
            `

<div class="product">

${item.product.name}

×

${item.quantity}


</div>

`;

    });


    box.innerHTML +=
        `

<button onclick="checkout()">

Заказать

</button>

`;


}


async function checkout() {


    await api(
        "/orders/",
        {
            method: "POST"
        }
    );


    alert(
        "Заказ создан"
    );


}


// ==========================
// ORDERS
// ==========================


async function loadOrders() {


    const orders =
        await api("/orders/");


    const box =
        document.getElementById("ordersBox");


    box.innerHTML = "";


    orders.forEach(o => {


        box.innerHTML +=
            `

<div class="product">

<h3>
Заказ №${o.id}
</h3>


<p>
${o.status}
</p>


<p>
${o.total_price} ֏
</p>


</div>

`;


    });

}

function toast(message, type="error"){


    const container =
        document.getElementById(
            "toastContainer"
        );


    const div =
        document.createElement("div");


    div.className =
        "toast " + type;


    div.innerText =
        message;


    container.appendChild(div);



    setTimeout(()=>{


        div.classList.add("hide");


        setTimeout(()=>{

            div.remove();

        },300);


    },3000);



}
loadProducts();