# Latest Indonesia Earthquake
Do you need the latest earthquake from BMKG | Indonesia Meteorological, Climatological, and Geophysical Agency

## Guidance
This package will scrape the latest earthquake data from [BMKG](https://www.bmkg.go.id/).

1. Install package from https://pypi.org/project/indonesia-earthquake/
2. Run your main.py with this code

```
import last_earthquake

if __name__ == '__main__':
    result = last_earthquake.data_extraction()
    last_earthquake.show_data(result)
```

# Author
Arsenius Anom Permadi