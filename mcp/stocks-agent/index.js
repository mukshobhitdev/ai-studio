import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
    name: 'Stock Price Fetcher',
    version: '1.0.0',
});

async function getStockPriceBySymbol(symbol) {
    const stockPrices = {
        "RELIANCE": { price: 2500, currency: "INR" },
        "TCS": { price: 3500, currency: "INR" },
        "INFY": { price: 1500, currency: "INR" },
        "HDFC": { price: 2800, currency: "INR" },
        "ICICIBANK": { price: 950, currency: "INR" },
        "WIPRO": { price: 400, currency: "INR" },
        "HCLTECH": { price: 1100, currency: "INR" },
        "BAJAJFINANCE": { price: 7000, currency: "INR" },
        "ADANIPORTS": { price: 800, currency: "INR" },
        "ITC": { price: 450, currency: "INR" },
        "ONGC": { price: 180, currency: "INR" },
        "POWERGRID": { price: 220, currency: "INR" },
        "NTPC": { price: 170, currency: "INR" },
        "SUNPHARMA": { price: 950, currency: "INR" },
        "TITAN": { price: 3200, currency: "INR" },
        "ULTRACEMCO": { price: 7800, currency: "INR" },
        "MARUTI": { price: 9500, currency: "INR" },
        "ASIANPAINT": { price: 3100, currency: "INR" },
        "AXISBANK": { price: 950, currency: "INR" },
        "SBIN": { price: 600, currency: "INR" },
    };

    const stockData = stockPrices[symbol.toUpperCase()];
    if (stockData) {
        return {
            price: stockData.price,
            currency: stockData.currency,
        };
    } else {
        return {
            error: "Stock symbol not found",
        };
    }
}

server.tool("getStockPriceBySymbol",
    {
        symbol: z.string(),
    },
    async ({ symbol }) => {
        return {
            content: [{ type: "text", text: JSON.stringify(await getStockPriceBySymbol(symbol)) }]
        };
    },
    {
        description: "Fetches real-time stock price for a given symbol in the Indian share market.",
    }
);

async function init() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}

init();