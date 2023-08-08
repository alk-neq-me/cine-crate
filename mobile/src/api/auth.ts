import axios from "axios";
import { ResponseUser } from "./types";


const BASE_URL = "http://192.168.100.206:8000/api/v1/"

export const authApi = axios.create({
  baseURL: BASE_URL,
  withCredentials: true
});

authApi.defaults.headers.common["Content-Type"] = "application/json";


authApi.interceptors.response.use(
  (response) => response,
  async (err) => {
    return Promise.reject(err)
  }
);


export async function signUpGuestUserFn(): Promise<ResponseUser> {
  const response = await authApi.post<ResponseUser>("guest-auth/register");
  return response.data;
}
