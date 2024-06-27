---
banner:
  title: "Support Center & Knowledge base"
  subtitle: "Find advice and answers from our support team fast or get in touch"
  bg_image: "images/banner.jpg"
  placeholder: "Have a question? Just ask here or enter terms"

cta:
  enable: false
  title: 'Installation'
  content: |
     The <code>opensees</code> package is hosted on <a href="https://pypi.org/project/opensees">PyPI</a>
     and can be installed by running

     <code>pip install opensees</code>
     <!--
     Source code is available on <a href="https://github.com/claudioperez/OpenSeesRT">GitHub</a>
     -->

  button:
    enable: false
    label: "contact us"
    link: "contact/"
---


<!-- topics -->
<div class="container">
  <div class="row justify-content-center">
    <div class="col-12 text-center">
      <h2 class="section-title">Collections</h2>
    </div>
      <div class="col-lg-4 col-sm-6 mb-4">
        <a
          href="./categories/basic/"
          class="px-4 py-5 bg-white shadow text-center d-block">
            <i class="{{ . }} icon text-primary d-block mb-4"></i>
          <h3 class="mb-3 mt-0">Introductory</h3>
            The basics of OpenSees
        </a>
      </div>
      <div class="col-lg-4 col-sm-6 mb-4">
        <a
          href="./examples/"
          class="px-4 py-5 bg-white shadow text-center d-block">
            <i class="{{ . }} icon text-primary d-block mb-4"></i>
          <h3 class="mb-3 mt-0">Modeling</h3>
            General model building.
        </a>
      </div>
      <div class="col-lg-4 col-sm-6 mb-4">
        <a
          href="./gallery/"
          class="px-4 py-5 bg-white shadow text-center d-block">
            <i class="{{ . }} icon text-primary d-block mb-4"></i>
          <h3 class="mb-3 mt-0">Gallery</h3>
            Examples of OpenSees in practice.
        </a>
      </div>
  </div>


  <h2 class=tabs-title>Ecosystem</h1>
  <div class=uikit-tab-wrapper>
    <table class="table">
      <thead>
          <tr class=highlight-th>
            <th scope="col"></td>
            <th scope="col">Package</td>
            <th scope="col">Description</td>
            <!-- </td> -->
          </tr>
      </thead>
      <tbody>
      <tr>
        <td style=text-align:center>
          <a href="https://github.com/claudioperez/opensees">
            <img style="max-width:100px; max-height: 30px; margin: 0"
                 src="https://chrystalchern.github.io/mdof/_static/images/content_images/brace/opensees.jpg" alt="opensees"></a></td>
        <td class=full-center-text><a href="https://pypi.org/project/opensees" />opensees</a></td>
        <td class=left-text>Direct and idiomatic bindings the 
          <a href="https://github.com/claudioperez/OpenSeesRT">OpenSeesRT</a> finite element analysis kernel.</td>
      </tr>
      <tr>
        <td style=text-align:center><img style="max-width:100px; max-height: 30px; margin: 0"
            src="https://chrystalchern.github.io/mdof/_static/images/content_images/brace/sdof.svg" alt="sdof"></td>
        <td class=full-center-text><a href="https://pypi.org/project/sdof" />sdof</a></td>
        <td class=left-text>Lightning-fast integration of single degree-of-freedom systems.</td>
      </tr>
      <tr>
        <td style=text-align:center><img style="max-width:100px; max-height: 30px; margin: 0"
            src="https://chrystalchern.github.io/mdof/_static/images/content_images/brace/mdof.svg" alt="mdof"></td>
        <td class=full-center-text><a href="https://pypi.org/project/mdof">mdof</a></td>
        <td class=left-text>Fast and friendly structural system identification.</td>
      </tr>
      <tr>
        <td style=text-align:center><img style="max-width:100px; max-height: 30px; margin: 0"
            src="https://chrystalchern.github.io/mdof/_static/images/content_images/brace/sees.png" alt="sees"></td>
        <td class=full-center-text><a href="https://pypi.org/project/sees">sees</a></td>
        <td class=left-text>Post-processing library built on modern web technologies.</td>
      </tr>
    </tbody>
    </table>
  </div>

</div>
