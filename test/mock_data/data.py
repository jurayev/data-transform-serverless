RAW_DICT = {
        "items": {
            "item": {
                "@id": "2445456",
                "@xmlns": {
                    "nsx": "http://www.w3.org/TR/html4/"
                },
                "category": "Jeans",
                "description": "Bootleg Front Washed",
                "images": {
                    "image": [
                        {
                            "@type": "1",
                            "@url": "https://sample.com/img/2445456_Image_1.jpg"
                        },
                        {},
                        {
                            "@type": "3",
                            "@url": "https://sample.com/img/2445456_Image_3.jpg"
                        }
                    ]
                },
                "prices": {
                    "price": [
                        {
                            "currency": "EUR",
                            "value": "49.95"
                        },
                        {
                            "currency": "DKK",
                            "value": "445.60"
                        }
                    ]
                }
            }
        }
    }

FORMATTED_DICT = {
    "products": [
        {
            "product_id": "2445456",
            "procduct_category": "Jeans",
            "product_description": "Bootleg Front Washed",
            "product_images": {
                "image_1": "https://sample.com/img/2445456_Image_1.jpg",
                "image_3": "https://sample.com/img/2445456_Image_3.jpg"
            },
            "prices": [
                {
                    "currency": "EUR",
                    "value": "49.95"
                },
                {
                    "currency": "DKK",
                    "value": "445.60"
                }
            ]
        }
    ]
}

FORMATTED_DICT_TWO_PRODUCTS = {
    "products": [
        [
            {
                "product_id": "2445456",
                "procduct_category": "Jeans",
                "product_description": "Bootleg Front Washed",
                "product_images": {
                    "image_1": "https://sample.com/img/2445456_Image_1.jpg",
                    "image_3": "https://sample.com/img/2445456_Image_3.jpg"
                },
                "prices": [
                    {
                        "currency": "EUR",
                        "value": "49.95"
                    },
                    {
                        "currency": "DKK",
                        "value": "445.60"
                    }
                ]
            },
            {
                "product_id": "123456",
                "procduct_category": "Jacket",
                "product_description": "Cool Jacket",
                "product_images": {
                    "image_1": "https://sample.com/img/2445456_Image_1.jpg",
                    "image_2": "https://sample.com/img/2445456_Image_2.jpg",
                    "image_3": "https://sample.com/img/2445456_Image_3.jpg"
                },
                "prices": [
                    {
                        "currency": "EUR",
                        "value": "50.95"
                    },
                    {
                        "currency": "USD",
                        "value": "30.50"
                    },
                    {
                        "currency": "DKK",
                        "value": "445.60"
                    }
                ]
            }
        ]
    ]
}

RULES = {"NameMapping": {"items": "products",
                          "id": "product_id",
                          "category": "procduct_category",
                          "description": "product_description",
                          "images": "product_images",
                          "url": "image"
                          },
         "TypeMapping": {"items": {"type": [], "depth_level": 1},
                          "images": {"type": {}, "depth_level": 2},
                          "prices": {"type": [], "depth_level": 2}
                          },
         "ignore": {"@xmlns", "@type"},
         "namespaces": {
             'http://www.w3.org/TR/html4/': None
         }
         }
