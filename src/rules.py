RULES = {"name mapping": {  "items": "products",
                            "id": "product_id",
                            "category": "procduct_category",
                            "description": "product_description",
                            "images": "product_images",
                            "url": "image"
                            },
        "type mapping": {  "items": {"type": [], "depth_level": 1},
                            "images": {"type": {}, "depth_level": 2},
                            "prices": {"type": [], "depth_level": 2}
                            },
        "ignore": {"@xmlns", "@type"},
        "namespaces": {
            'http://www.w3.org/TR/html4/': None
        }
    }