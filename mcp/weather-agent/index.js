import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
    name: 'weather Fetcher',
    version: '1.0.0',
});

async function getWeatherByCityName(city) {
    const url =`http://api.weatherapi.com/v1/current.json?key=a745d8dfc69f472781335623252104&q=${city}&aqi=no`

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Error fetching weather data: ${response.statusText}`);
        }

        const data = await response.json();
        return {
            temperature: data.current.temp_c,
            weather: data.current.condition.text,
        };
    } catch (error) {
        console.error(error);
        return {
            temperature: null,
            weather: "no data found",
        };
    }

}


server.tool("getWeatherByCityName",
    {
        city: z.string(),
    },
    async ({ city }) => {
       return {
        content: [{ type: "text", text: JSON.stringify(await getWeatherByCityName(city)) }]
       }
    },
  {
    description: "Fetches weather information (temperature and conditions) for a given city name.",
  }
);

async function init() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
}

init();
