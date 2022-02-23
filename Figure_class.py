class Figure:
    def __init__(self, filtered_data, cripto):
        self.filtered_data = filtered_data
        self.cripto = cripto

    def build (self):
        return {
                "data": [
                    {
                        "x": self.filtered_data.index,
                        "y": self.filtered_data["price"],
                        "type": "lines",
                        "name": "Cotización",
                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                    },
                    {
                        "x": self.filtered_data.index,
                        "y": self.filtered_data["vwap"],
                        "type": "lines",
                        "name": "VWAP",
                        "hovertemplate": "$%{y:.2f}<extra></extra>",
                    },
                ],
                "layout": {
                    "title": {
                        "text": "Cotización y VWAP de la criptomoneda: {}".format(self.cripto),
                        "x": 0.05,
                        "xanchor": "left",
                    },
                    "xaxis": {"fixedrange": True},
                    "yaxis": {"tickprefix": "$", "fixedrange": True},
                    "colorway": ["#ecaf13", "#de5f08"],
                },
        }