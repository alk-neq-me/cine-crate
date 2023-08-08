import axios from "axios";

export async function root(): Promise<string> {
  const data = await axios.get<{message: string; status: number}>("http://192.168.100.206:8000/").then(res => res.data).catch(e => {throw new Error(e)});
  return data.message;
}
