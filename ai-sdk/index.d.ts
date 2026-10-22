import type { Tool } from 'ai';

export interface TableJourneyOptions {
  /** Optional partner key: tags every booking link with your partner code. Defaults to process.env.TABLEJOURNEY_API_KEY. */
  apiKey?: string;
  /** MCP endpoint. Defaults to https://tablejourney.com/mcp. */
  endpoint?: string;
}

export declare function tablejourneyTools(options?: TableJourneyOptions): {
  thingsToDo: Tool;
  searchPlaces: Tool;
  festivals: Tool;
  experiences: Tool;
  stays: Tool;
  dishes: Tool;
  cities: Tool;
};

export default tablejourneyTools;
