<script>
  import { link } from "svelte-routing";

  // core components
  import IndexDropdown from "components/Dropdowns/IndexDropdown.svelte";

  let navbarOpen = false;

  function setNavbarOpen() {
    navbarOpen = !navbarOpen;
  }
</script>

<nav
  class="top-0 fixed z-50 w-full flex flex-wrap items-center justify-between px-2 py-3 navbar-expand-lg bg-white shadow"
>
  <div
    class="container px-4 mx-auto flex flex-wrap items-center justify-between"
  >
    <div
      class="w-full relative flex justify-between lg:w-auto lg:static lg:block lg:justify-start"
    >
      <a
        use:link
        class="text-gray-800 text-sm font-bold leading-relaxed inline-block mr-4 py-2 whitespace-no-wrap uppercase"
        href="/"
      >
        RMobile 
      </a>
      <button
        class="cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
        type="button"
        on:click="{setNavbarOpen}"
      >
        <i class="fas fa-bars"></i>
      </button>
    </div>
    <div
      class="lg:flex flex-grow items-center {navbarOpen ? 'block':'hidden'}"
      id="example-navbar-warning"
    >
      <ul class="flex flex-col lg:flex-row list-none lg:ml-auto">

        <li class="flex items-center">
          <a
            class="hover:text-gray-600 text-gray-800 px-3 py-2 flex items-center text-xs uppercase font-bold"
            href="https://github.com/Parinz/"
            target="_blank"
          >
            <i class="text-gray-500 fab fa-github text-lg leading-lg" />
            <span class="lg:hidden inline-block ml-2">Star</span>
          </a>
        </li>
      </ul>
    </div>
  </div>
</nav>
