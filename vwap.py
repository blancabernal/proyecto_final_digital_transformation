def vwap(data):
    volume = data.volume.values
    price = data.price.values
    return data.assign(vwap=(volume * price).cumsum() / volume.cumsum())

