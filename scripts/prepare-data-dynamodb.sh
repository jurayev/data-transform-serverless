#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

chmod +x scripts/set-vars.sh
. scripts/set-vars.sh

# put a new item
aws --endpoint-url=$AWS_ENDPOINT dynamodb put-item \
    --region=$AWS_REGION \
    --table-name rulesTable  \
    --item \
     '
    {"RuleId": {"N": "1"},
     "NameMapping": {"M": {"items": {"S": "products"},
                           "id": {"S": "product_id"},
                           "category": {"S": "product_category"},
                           "description": {"S": "product_description"},
                           "images": {"S": "product_images"},
                           "url": {"S": "image"}}
                     },
     "TypeMapping": {"M": {"items": {"M":
                                         {"type": {"L": []},
                                          "depth_level": {"N": "1"}
                                          }
                                     },
                           "images": {"M":
                                         {"type": {"M": {}},
                                          "depth_level": {"N": "2"}
                                          }
                                     },
                           "prices": {"M":
                                         {"type": {"L": []},
                                          "depth_level": {"N": "2"}
                                          }
                                     }
                           }},
      "ignore": {"M": {"@xmlns": {"BOOL": true},
                      "@type": {"BOOL": true}
                      }
                },
      "namespaces": {"M": {"http://www.w3.org/TR/html4/": {"NULL": true}
                          }
                    }
      }
      '
