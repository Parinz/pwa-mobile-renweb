<script>
  import { Link } from "svelte-routing";

  // core components
  import IndexNavbar from "components/Navbars/IndexNavbar.svelte";
  import Footer from "components/Footers/Footer.svelte";

  const patternVue = "/assets/img/pattern_svelte.png";
  export let location;


  import { onMount } from 'svelte';
  let text = "better.";
  const Sleep = (ms) => {return new Promise(resolve => setTimeout(resolve, ms));}
  const Advantages = async () => {
      let advantage = ["faster.", "modern.", "Free."]
      for (let i = 0; i < 3; i++) {
          text = advantage[i]
          await Sleep(2000)
        }
      } 
  onMount(Advantages)
</script>

<IndexNavbar />
<section class="header relative pt-16 items-center flex h-screen max-h-860-px">
  <div class="container mx-auto items-center flex flex-wrap">
    <div class="w-full md:w-8/12 lg:w-6/12 xl:w-6/12 px-4">
      <div class="pt-32 sm:pt-0">
        <h2 class="font-semibold text-4xl text-gray-700">
          RMobile - { text }
        </h2>
        <p class="mt-4 text-lg leading-relaxed text-gray-600">
          <b>RMobile</b> is a free, fast and modern rewrite of the Renweb App for mobile. RMobile provides a simple UI with easy to use buttons. It also supports Thai language as well.
        </p>
        <div class="mt-12">
          <a
            href="/auth/login/"
            class="get-started text-white font-bold px-6 py-4 rounded outline-none focus:outline-none mr-1 mb-1 bg-red-500 active:bg-red-600 uppercase text-sm shadow hover:shadow-lg ease-linear transition-all duration-150"
          >
            Get started
          </a>
        </div>
      </div>
    </div>
  </div>

  <img
    class="absolute top-0 b-auto right-0 pt-16 sm:w-6/12 -mt-48 sm:mt-0 w-10/12 max-h-860-px"
    src="{patternVue}"
    alt="..."
  />
</section>

<section class="mt-48 md:mt-40 pb-40 relative bg-gray-200">
  <div
    class="-mt-20 top-0 bottom-auto left-0 right-0 w-full absolute h-20"
    style="transform: translateZ(0);"
  >
    <svg
      class="absolute bottom-0 overflow-hidden"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="none"
      version="1.1"
      viewBox="0 0 2560 100"
      x="0"
      y="0"
    >
      <polygon
        class="text-gray-200 fill-current"
        points="2560 0 2560 100 0 100"
      ></polygon>
    </svg>
  </div>
  <div class="container mx-auto">
    <div class="flex flex-wrap items-center">
      <div class="w-full md:w-6/12 px-4">
        <div class="flex flex-wrap">
          <div class="w-full md:w-6/12 px-4">
            <div class="relative flex flex-col mt-4">
              <div class="px-4 py-5 flex-auto">
                <div
                  class="text-gray-600 p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-white"
                >
                  <i class="fas fa-sitemap"></i>
                </div>
                <h6 class="text-xl mb-1 font-semibold">
                  Free
                </h6>
                <p class="mb-4 text-gray-600">
                  RMobile is a free-to-use software
                </p>
              </div>
            </div>
            <div class="relative flex flex-col min-w-0">
              <div class="px-4 py-5 flex-auto">
                <div
                  class="text-gray-600 p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-white"
                >
                  <i class="fas fa-drafting-compass"></i>
                </div>
                <h6 class="text-xl mb-1 font-semibold">
                  No-Install
                </h6>
                <p class="mb-4 text-gray-600">
                  Just add to home screen! No need to download from app store.
                </p>
              </div>
            </div>
          </div>
          <div class="w-full md:w-6/12 px-4">
            <div class="relative flex flex-col min-w-0 mt-4">
              <div class="px-4 py-5 flex-auto">
                <div
                  class="text-gray-600 p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-white"
                >
                  <i class="fas fa-newspaper"></i>
                </div>
                <h6 class="text-xl mb-1 font-semibold">Easy to Use</h6>
                <p class="mb-4 text-gray-600">
                  RMobile is easy to use with its clear interface, and large buttons.
                </p>
              </div>
            </div>
            <div class="relative flex flex-col min-w-0">
              <div class="px-4 py-5 flex-auto">
                <div
                  class="text-gray-600 p-3 text-center inline-flex items-center justify-center w-12 h-12 mb-5 shadow-lg rounded-full bg-white"
                >
                  <i class="fas fa-file-alt"></i>
                </div>
                <h6 class="text-xl mb-1 font-semibold">
                  Multi-Language
                </h6>
                <p class="mb-4 text-gray-600">
                  RMobile supports both Thai and English allowing for it to be widely available.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="block relative z-1 bg-gray-700">
  <div class="container mx-auto">
    <div class="justify-center flex flex-wrap">
      <div class="w-full lg:w-12/12 px-4 -mt-24">
        <div class="flex flex-wrap">
          <div class="w-full lg:w-12/12 px-4">
            <h5 class="text-xl font-semibold pb-4 text-center">
              How To Use
            </h5>
              <div
                class="hover:-mt-4 relative flex flex-col min-w-0 break-words bg-white w-full mb-6 shadow-lg rounded-lg ease-linear transition-all duration-150"
              >
              <iframe title="ManDances" height="400" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen></iframe>
              </div>
        </div>
      </div>
    </div>
  </div>
</section>

<Footer />
