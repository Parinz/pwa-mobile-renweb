<script>
  import { onMount } from 'svelte';
  let text = "better.";
  const Sleep = (ms) => {return new Promise(resolve => setTimeout(resolve, ms));}
  const Advantages = async () => {
      let advantage = ["faster.", "modern.", "Free, forever."]
      for (let i = 0; i < 3; i++) {
          text = advantage[i]
          await Sleep(2000)
        }
      } 
  onMount(Advantages)
</script>


<div class="parallax">
  <div class="textBox">
    <span class="text"><h1>Renweb for Mobile that is <strong>{ text }</strong> </h1></span>
  </div>
</div>

<style>
  body, html {
  height: 100%;
}

.parallax {
  /* The image used */
  background-image: url("./img/parralax.jpg"); 

  /* Full height */
  height: 100%;

  /* Create the parallax scrolling effect */
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
}

.textBox {
  position: absolute;
  left: 0;
  top: 50%;
  width: 100%;
  text-align: center;
  color: grey;
}

.text {
  background-color: black;
  color: white;
  padding: 18px;
  font-size: 25px;
  letter-spacing: 10px;
}
</style>
