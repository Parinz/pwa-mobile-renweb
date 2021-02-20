<script>
  import { link } from "svelte-routing";

  // core components
  const github = "../assets/img/github.svg";
  const google = "../assets/img/google.svg";
  export let location;


  let districtCode;
  let username;
  let password;
  let processing = true;
    const handleSignIn = async (districtCode, username, password) =>  {
        await fetch(`http://renweb-redesigned.herokuapp.com/auth/${districtCode}/${username}/${password}/`)
      .then(r => r.json())
      .then(data => {
      let result = data;
      console.log(result)
        });
      }
</script>

<div class="container mx-auto px-4 h-full">
  <div class="flex content-center items-center justify-center h-full">
    <div class="w-full lg:w-4/12 px-4">
      <div
        class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0"
      >
        <div class="rounded-t mb-0 px-6 py-6">
          <hr class="mt-6 border-b-1 border-gray-400" />
        </div>
        <div class="flex-auto px-4 lg:px-10 py-10 pt-0">
          <form>
            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-gray-700 text-xs font-bold mb-2"
                for="grid-districtCode"
              >
                District Code
              </label>

              <input
                id="grid-districtCode"
                type="email"
                class="px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:shadow-outline w-full ease-linear transition-all duration-150"
                placeholder="District-Code"
                bind:value={districtCode}
              />
            </div>

            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-gray-700 text-xs font-bold mb-2"
                for="grid-username"
              >
                Username
              </label>

              <input
                id="grid-username"
                type="email"
                class="px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:shadow-outline w-full ease-linear transition-all duration-150"
                placeholder="Username"
                bind:value={username}
              />
            </div>

            <div class="relative w-full mb-3">
              <label
                class="block uppercase text-gray-700 text-xs font-bold mb-2"
                for="grid-password"
              >
                Password
              </label>
              <input
                id="grid-password"
                type="password"
                class="px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:shadow-outline w-full ease-linear transition-all duration-150"
                placeholder="Password"
                bind:value={password}
              />
            </div>
            <div class="text-center mt-6">
              <button
                class="bg-gray-900 text-white active:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full ease-linear transition-all duration-150"
                type="button"
                on:click={handleSignIn(districtCode, username, password)}
              >
                Sign In
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
