#define CPPHTTPLIB_OPENSSL_SUPPORT
#include "httplib.h"
#include <cuda_runtime.h>
#include <nvtx3/nvToolsExt.h>
#include <iostream>
#include <random>
#include <cmath>
#include <stdio.h>
using namespace std;



int main() {
cout<< "57" <<endl;
return 0;
}

// httplib::Headers headers(const Environment& environment) {
//   return {
//       {"APCA-API-KEY-ID", environment.getAPIKeyID()},
//       {"APCA-API-SECRET-KEY", environment.getAPISecretKey()},
//   };
// }

// std::pair<Status, Account> Client::getAccount() const {
//   Account account;

//   httplib::SSLClient client(environment_.getAPIBaseURL());
//   auto resp = client.Get("/v2/account", headers(environment_));
//   if (!resp) {
//     return std::make_pair(Status(1, "Call to /v2/account returned an empty response"), account);
//   }
// }