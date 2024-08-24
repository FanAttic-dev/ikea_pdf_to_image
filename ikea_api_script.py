import ikea_api
from ikea_api import run

# Constants like country, language, base url
constants = ikea_api.Constants(country="gb", language="en")

endpoint = ikea_api.Auth(constants).get_guest_token()
token = run(endpoint)

item_id = "70340826"

cart = ikea_api.Cart(constants, token=token)
order = ikea_api.OrderCapture(constants, token=token)

# cart.add_items({item_id: 1})

cart_show = run(cart.show())

items = ikea_api.convert_cart_to_checkout_items(cart_show)

checkout_id = run(order.get_checkout(items))
service_area_id = run(
    order.get_service_area(
        checkout_id,
        zip_code="02215",
        state_code="MA",  # pass State Code only if your country has them
    )
)
home_services = run(order.get_home_delivery_services(checkout_id, service_area_id))
collect_services = run(
    order.get_collect_delivery_services(checkout_id, service_area_id)
)

# res = ikea_api.run(endpoint)
# print("hello")