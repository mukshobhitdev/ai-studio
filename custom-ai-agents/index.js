import dotenv from 'dotenv';
import sql from 'mssql';
import { AzureOpenAI } from "openai";
import readlineSync from 'readline-sync';

dotenv.config();

const DEPLOYMENT_NAME = process.env.DEPLOYMENT_NAME;
const API_VERSION = process.env.API_VERSION;

const config = {
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    server: process.env.DB_SERVER,
    database: process.env.DB_DATABASE,
    options: {
        encrypt: false
    }
};

async function getProductById(id) {
    try {
        let pool = await sql.connect(config);
        let result = await pool.request()
            .input('Id', sql.Int, id)
            .query('SELECT Id, Name, Description, CreatedOn FROM Products WHERE Id = @Id');
        return result.recordset[0];
    } catch (err) {
        console.error('SQL error', err);
    }
}

async function deleteProductById(id) {
    try {
        let pool = await sql.connect(config);
        await pool.request()
            .input('Id', sql.Int, id)
            .query('DELETE FROM Products WHERE Id = @Id');
        console.log(`Product with Id ${id} deleted successfully.`);
    } catch (err) {
        console.error('SQL error', err);
    }
}

async function createProduct(input) {
    try {
        let pool = await sql.connect(config);
        let result = await pool.request()
            .input('Name', sql.NVarChar, input.name)
            .input('Description', sql.NVarChar, input.description)
            .input('CreatedOn', sql.DateTime, new Date())
            .query('INSERT INTO Products (Name, Description, CreatedOn) OUTPUT INSERTED.Id VALUES (@Name, @Description, @CreatedOn)');
        return result.recordset[0].Id;
    } catch (err) {
        console.error('SQL error', err);
    }
}

async function searchProduct(keyword) {
    try {
        let pool = await sql.connect(config);
        let result = await pool.request()
            .input('Keyword', sql.NVarChar, `%${keyword}%`)
            .query('SELECT * FROM Products WHERE Name LIKE @Keyword OR Description LIKE @Keyword');
        return result.recordset;
    } catch (err) {
        console.error('SQL error', err);
    }
}

async function getAllProducts() {
    try {
        let pool = await sql.connect(config);
        let result = await pool.request()
            .query('SELECT * FROM Products');
        return result.recordset;
    } catch (err) {
        console.error('SQL error', err);
    }
}

const client = new AzureOpenAI({ DEPLOYMENT_NAME, API_VERSION });

async function callAzureOpenAI(messages) {
    try {
        const events = await client.chat.completions.create({
            messages: messages,
            max_tokens: 3000,
            model: DEPLOYMENT_NAME,
        });

        return  events.choices[0].message.content;
    } catch (error) {
        console.error("Error:", error);
        if (error.status === 404) {
            console.error("Resource not found. Please check the endpoint URL and resource availability.");
        }
    }
}

(async () => {

    const tools = {
        createProduct:createProduct,
        searchProduct:searchProduct,
        getProductById:getProductById,
        deleteProductById:deleteProductById,
        getAllProducts:getAllProducts
    }

    const SYSTEM_PROMPT = `
    You can manage Products by ADD, DELETE, SEARCH and GET operations on products. You Must strictly follow 
    the JSON output format.

    You are an AI Product Assistant with START, PLAN, ACTION, OBSERVATION and Output State.
    Wait for the user prompt and first Plan using available tools.
    After planning, Take the action with appropriate tools and wait for Observation based on Actions.
    Once you get the observations, return the AI response based on START prompt and observations

    Products Table Schema:
    - Id (int) and Primary Key
    - Name (nvarchar)
    - Description (nvarchar)
    - CreatedOn (datetime)
    
    Available Tools:
    - searchProduct(keyword): Search for a product by name or description
    - getProductById(id): Get a product by its Id
    - createProduct(name, description): Create a new product in database and takes name and desciption of Product
    - deleteProductById(id): Delete a product by its Id
    - getAllProducts(): Get all products from database

    Example:
    START
    {"type", "user", "user": "Add a Product name and description'"}
    {"type", "plan", "plan": "I will try to get more context on what product to add."}
    {"type", "output", "output": "What is the product name and description?"}
    {"type", "user", "user": "I want to add a product 'Maggy' with  description 'ready in 2 minutes'"}
    {"type", "plan", "plan": "I will add the product with the name and description."}
    {"type", "action", "function": "createProduct", "input": {"name": "Maggy", "description": "ready in 2 minutes"}}
    {"type", "observation", "observation": "1001"}
    {"type", "output", "output": "Product added successfully with Id 1001"}
    `;
    
    const messages=[{role: "system", content: SYSTEM_PROMPT}];

    while (true) {

        const query= readlineSync.question('>> ');
        const userMessage = {role: "user", content: query};

        messages.push({role: "user", content: JSON.stringify(userMessage)});

        while (true) {
            const result= await callAzureOpenAI(messages);

            messages.push({role: "assistant", content: result});

            const action = JSON.parse(result);

            if(action.type==="output"){
                console.log(action.output);
                break;
            }
            else if(action.type==="action"){
                const fn=tools[action.function];

                if(!fn) throw new Error(`Function ${action.function} not found`);

                const observation =await fn(action.input);

                const observationMessage = {
                    type: "observation",
                    observation: observation
                };

                messages.push({role: "assistant", content: JSON.stringify(observationMessage)});

            }

        }
    }
    // let productId=await createProduct('Sample Product', 'This is a sample mobile.');
    // const product = await getProductById(productId);

    // let searchResponse= await searchProduct('sample');
    // console.log(searchResponse);
    // await deleteProductById(1);
})();
