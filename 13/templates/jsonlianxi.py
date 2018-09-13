a={
  "apps_count": 6,
  "page_size": 20,
  "items": [
    {
      "id": "59bf8e26959d69523e000177",
      "user_id": "XXXXXX",
      "org_id": "59bba986548b7a1688812a7c",
      "type": "android",
      "name": "yljk",
      "short": "yx9a",
      "bundle_id": "XXXXXX",
      "genre_id": 0,
      "is_opened": false,
      "web_template": "default",
      "custom_market_url": "",
      "has_combo": false,
      "created_at": 1505725990,
      "updated_at": 1505726002,
      "expired_at": 1505898802,
      "icon_url": "https://XXXXXX.com",
      "master_release": {
        "version": "1.0.0",
        "build": "1",
        "release_type": "inhouse",
        "distribution_name": "",
        "supported_platform": null,
        "created_at": XXXXXX
      }
    },
    {
      "id": "XXXXXX",
      "user_id": "XXXXXX",
      "org_id": "XXXXXX",
      "type": "android",
      "name": "wld",
      "short": "bpdb",
      "bundle_id": "XXXXXX",
      "genre_id": 0,
      "is_opened": false,
      "web_template": "default",
      "custom_market_url": "",
      "has_combo": false,
      "created_at": XXXXXX,
      "updated_at": XXXXXX,
      "expired_at": XXXXXX,
      "icon_url": "https://XXXXXX.com",
      "master_release": {
        "version": "1.0.0",
        "build": "1",
        "release_type": "inhouse",
        "distribution_name": "",
        "supported_platform": null,
        "created_at": XXXXXX
      }
    },
    {
      "id": "XXXXXX",
      "user_id": "XXXXXX",
      "org_id": "XXXXXX",
      "type": "android",
      "name": "wzlj",
      "short": "1tdc",
      "bundle_id": "XXXXXX",
      "genre_id": 0,
      "is_opened": false,
      "web_template": "default",
      "custom_market_url": "",
      "has_combo": false,
      "created_at": XXXXXX,
      "updated_at": XXXXXX,
      "expired_at": XXXXXX,
      "icon_url": "https://XXXXXX.com",
      "master_release": {
        "version": "1.0.0",
        "build": "1",
        "release_type": "inhouse",
        "distribution_name": "",
        "supported_platform": null,
        "created_at": XXXXXX
      }
    },
    {
      "id": "XXXXXX",
      "user_id": "XXXXXX",
      "org_id": "XXXXXX",
      "type": "android",
      "name": "maib",
      "short": "y6td",
      "bundle_id": "XXXXXX",
      "genre_id": 0,
      "is_opened": false,
      "web_template": "default",
      "custom_market_url": "",
      "has_combo": false,
      "created_at": XXXXXX,
      "updated_at": XXXXXX,
      "expired_at": XXXXXX,
      "icon_url": "https://XXXXXX.com",
      "master_release": {
        "version": "1.0.0",
        "build": "1",
        "release_type": "inhouse",
        "distribution_name": "",
        "supported_platform": null,
        "created_at": XXXXXX
      }
    },
    {
      "id": "XXXXXX",
      "user_id": "XXXXXX",
      "org_id": "XXXXXX",
      "type": "android",
      "name": "jieb",
      "short": "jg3e",
      "bundle_id": "XXXXXX",
      "genre_id": 0,
      "is_opened": false,
      "web_template": "default",
      "custom_market_url": "",
      "has_combo": false,
      "created_at": XXXXXX,
      "updated_at": XXXXXX,
      "expired_at": XXXXXX,
      "icon_url": "https://XXXXXX.com",
      "master_release": {
        "version": "1.0.0",
        "build": "1",
        "release_type": "inhouse",
        "distribution_name": "",
        "supported_platform": null,
        "created_at": XXXXXX
      }
    },
    {
      "id": "XXXXXX",
      "user_id": "XXXXXX",
      "org_id": "XXXXXX",
      "type": "android",
      "name": "xxdk",
      "short": "5ewf",
      "bundle_id": "XXXXXX",
      "genre_id": 0,
      "is_opened": false,
      "web_template": "default",
      "custom_market_url": "",
      "has_combo": false,
      "created_at": XXXXXX,
      "updated_at": XXXXXX,
      "expired_at": XXXXXX,
      "icon_url": "https://XXXXXX.com",
      "master_release": {
        "version": "1.0.0",
        "build": "1",
        "release_type": "inhouse",
        "distribution_name": "",
        "supported_platform": null,
        "created_at": XXXXXX
      }
    }
  ]
}

import json
data = json.load(file)
result = [(item.get('name', 'NA'), item.get('short', 'NA')) for item in data['items']]