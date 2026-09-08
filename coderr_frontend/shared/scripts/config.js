const GUEST_LOGINS = {
  customer: {
    username: "andrey",
    password: "asdasd",
  },
  business: {
    username: "kevin",
    password: "asdasd24",
  },
};

const isLocalhost =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1";

export const API_BASE_URL = isLocalhost
  ? "http://127.0.0.1:8000/api/"
  : "https://coderr-v4g3.onrender.com/api/";

export const STATIC_BASE_URL = isLocalhost
  ? "http://127.0.0.1:8000/"
  : "https://coderr-v4g3.onrender.com/";

const LOGIN_URL = "login/";

const REGISTER_URL = "registration/";

const PROFILE_URL = "profile/";

const BUSINESS_PROFILES_URL = "profiles/business/";

const CUSTOMER_PROFILES_URL = "profiles/customer/";

const REVIEW_URL = "reviews/";

const ORDER_URL = "orders/";

const OFFER_URL = "offers/";

const OFFER_DETAIL_URL = "offerdetails/";

const BASE_INFO_URL = "base-info/";

const OFFER_INPROGRESS_COUNT_URL = "order-count/";
const OFFER_COMPLETED_COUNT_URL = "completed-order-count/";

const PAGE_SIZE = 6;
