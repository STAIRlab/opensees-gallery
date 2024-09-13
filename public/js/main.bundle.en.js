const alert = document.getElementById('page-alert')
const closeBtn = document.getElementById('page-alert-btn-close')
if (alert !== null && closeBtn !== null) {
  const version = alert.getAttribute('data-page-alert-version') || 'unknown'
  const hideAlert = sessionStorage.getItem(`page-alert-${version}`) !== null
  if (hideAlert) {
    alert.classList.add('d-none')
  }

  closeBtn.addEventListener('click', () => {
    sessionStorage.setItem(`page-alert-${version}`, 'seen')
    alert.classList.add('d-none')
  })
}

;
// Adapted from https://github.com/gohugoio/hugo/blob/master/tpl/tplimpl/embedded/templates/google_analytics.html


;
function reveal () {
  const reveals = document.querySelectorAll('.reveal')

  for (let i = 0; i < reveals.length; i++) {
    const windowHeight = window.innerHeight
    const elementTop = reveals[i].getBoundingClientRect().top
    const elementVisible = 150

    if (elementTop < windowHeight - elementVisible) {
      reveals[i].classList.add('active')
      reveals[i].classList.remove('reveal')
    } else {
      reveals[i].classList.remove('active')
    }
  }
}

window.addEventListener('scroll', reveal)

;
/*
Source:
  - https://simplernerd.com/hugo-add-copy-to-clipboard-button/
*/

const svgCopy =
  '<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16"><path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/><path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"/></svg>'
const svgCheck =
  '<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true"><path fill-rule="evenodd" fill="rgb(63, 185, 80)" d="M13.78 4.22a.75.75 0 010 1.06l-7.25 7.25a.75.75 0 01-1.06 0L2.22 9.28a.75.75 0 011.06-1.06L6 10.94l6.72-6.72a.75.75 0 011.06 0z"></path></svg>'

const addCopyButtons = (clipboard) => {
  // 1. Look for pre > code elements in the DOM
  document.querySelectorAll('pre > code').forEach((codeBlock) => {
    // 2. Create a button that will trigger a copy operation
    const button = document.createElement('button')
    button.className = 'clipboard-button'
    button.setAttribute('data-toast-target', 'toast-copied-code-message')
    button.setAttribute('aria-label', 'copy to clipboard')
    button.type = 'button'
    button.innerHTML = svgCopy
    button.addEventListener('click', () => {
      const text = codeBlock.innerText.split('\n').filter(Boolean).join('\n')
      clipboard.writeText(text).then(
        () => {
          button.blur()
          button.innerHTML = svgCheck
          setTimeout(() => (button.innerHTML = svgCopy), 2000)
        },
        // eslint-disable-next-line n/handle-callback-err
        (error) => (button.innerHTML = 'Error')
      )
    })
    // 3. Append the button directly before the pre tag
    const pre = codeBlock.parentNode
    pre.parentNode.insertBefore(button, pre)
  })
}

if (navigator && navigator.clipboard) {
  addCopyButtons(navigator.clipboard)
}

document.querySelectorAll('[data-clipboard]').forEach(trigger => {
  const text = trigger.getAttribute('data-clipboard')
  trigger.addEventListener('click', () => {
    navigator.clipboard.writeText(text)
  })
})

;
const url = new URL(window.location.href)
const menu = url.searchParams.get('menu')
const child = url.searchParams.get('child')
const menuItems = document.querySelectorAll('[data-nav="main"]')

if (menu !== null) {
  menuItems.forEach(element => {
    element.classList.remove('active')
  })

  const targetMainItems = document.querySelectorAll(`[data-nav-main="${menu}"]:not([data-nav-child])`)
  targetMainItems.forEach(element => {
    element.classList.add('active')
  })

  const targetChildItems = document.querySelectorAll(`[data-nav-main="${menu}"][data-nav-child="${child}"]`)
  targetChildItems.forEach(element => {
    element.classList.add('active')
  })
}

;
/*!
  * Bootstrap v5.3.3 (https://getbootstrap.com/)
  * Copyright 2011-2024 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
  */
(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.bootstrap = factory());
})(this, (function () { 'use strict';

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/data.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  /**
   * Constants
   */

  const elementMap = new Map();
  const Data = {
    set(element, key, instance) {
      if (!elementMap.has(element)) {
        elementMap.set(element, new Map());
      }
      const instanceMap = elementMap.get(element);

      // make it clear we only want one instance per element
      // can be removed later when multiple key/instances are fine to be used
      if (!instanceMap.has(key) && instanceMap.size !== 0) {
        // eslint-disable-next-line no-console
        console.error(`Bootstrap doesn't allow more than one instance per element. Bound instance: ${Array.from(instanceMap.keys())[0]}.`);
        return;
      }
      instanceMap.set(key, instance);
    },
    get(element, key) {
      if (elementMap.has(element)) {
        return elementMap.get(element).get(key) || null;
      }
      return null;
    },
    remove(element, key) {
      if (!elementMap.has(element)) {
        return;
      }
      const instanceMap = elementMap.get(element);
      instanceMap.delete(key);

      // free up element references if there are no instances left for an element
      if (instanceMap.size === 0) {
        elementMap.delete(element);
      }
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/index.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const MAX_UID = 1000000;
  const MILLISECONDS_MULTIPLIER = 1000;
  const TRANSITION_END = 'transitionend';

  /**
   * Properly escape IDs selectors to handle weird IDs
   * @param {string} selector
   * @returns {string}
   */
  const parseSelector = selector => {
    if (selector && window.CSS && window.CSS.escape) {
      // document.querySelector needs escaping to handle IDs (html5+) containing for instance /
      selector = selector.replace(/#([^\s"#']+)/g, (match, id) => `#${CSS.escape(id)}`);
    }
    return selector;
  };

  // Shout-out Angus Croll (https://goo.gl/pxwQGp)
  const toType = object => {
    if (object === null || object === undefined) {
      return `${object}`;
    }
    return Object.prototype.toString.call(object).match(/\s([a-z]+)/i)[1].toLowerCase();
  };

  /**
   * Public Util API
   */

  const getUID = prefix => {
    do {
      prefix += Math.floor(Math.random() * MAX_UID);
    } while (document.getElementById(prefix));
    return prefix;
  };
  const getTransitionDurationFromElement = element => {
    if (!element) {
      return 0;
    }

    // Get transition-duration of the element
    let {
      transitionDuration,
      transitionDelay
    } = window.getComputedStyle(element);
    const floatTransitionDuration = Number.parseFloat(transitionDuration);
    const floatTransitionDelay = Number.parseFloat(transitionDelay);

    // Return 0 if element or transition duration is not found
    if (!floatTransitionDuration && !floatTransitionDelay) {
      return 0;
    }

    // If multiple durations are defined, take the first
    transitionDuration = transitionDuration.split(',')[0];
    transitionDelay = transitionDelay.split(',')[0];
    return (Number.parseFloat(transitionDuration) + Number.parseFloat(transitionDelay)) * MILLISECONDS_MULTIPLIER;
  };
  const triggerTransitionEnd = element => {
    element.dispatchEvent(new Event(TRANSITION_END));
  };
  const isElement$1 = object => {
    if (!object || typeof object !== 'object') {
      return false;
    }
    if (typeof object.jquery !== 'undefined') {
      object = object[0];
    }
    return typeof object.nodeType !== 'undefined';
  };
  const getElement = object => {
    // it's a jQuery object or a node element
    if (isElement$1(object)) {
      return object.jquery ? object[0] : object;
    }
    if (typeof object === 'string' && object.length > 0) {
      return document.querySelector(parseSelector(object));
    }
    return null;
  };
  const isVisible = element => {
    if (!isElement$1(element) || element.getClientRects().length === 0) {
      return false;
    }
    const elementIsVisible = getComputedStyle(element).getPropertyValue('visibility') === 'visible';
    // Handle `details` element as its content may falsie appear visible when it is closed
    const closedDetails = element.closest('details:not([open])');
    if (!closedDetails) {
      return elementIsVisible;
    }
    if (closedDetails !== element) {
      const summary = element.closest('summary');
      if (summary && summary.parentNode !== closedDetails) {
        return false;
      }
      if (summary === null) {
        return false;
      }
    }
    return elementIsVisible;
  };
  const isDisabled = element => {
    if (!element || element.nodeType !== Node.ELEMENT_NODE) {
      return true;
    }
    if (element.classList.contains('disabled')) {
      return true;
    }
    if (typeof element.disabled !== 'undefined') {
      return element.disabled;
    }
    return element.hasAttribute('disabled') && element.getAttribute('disabled') !== 'false';
  };
  const findShadowRoot = element => {
    if (!document.documentElement.attachShadow) {
      return null;
    }

    // Can find the shadow root otherwise it'll return the document
    if (typeof element.getRootNode === 'function') {
      const root = element.getRootNode();
      return root instanceof ShadowRoot ? root : null;
    }
    if (element instanceof ShadowRoot) {
      return element;
    }

    // when we don't find a shadow root
    if (!element.parentNode) {
      return null;
    }
    return findShadowRoot(element.parentNode);
  };
  const noop = () => {};

  /**
   * Trick to restart an element's animation
   *
   * @param {HTMLElement} element
   * @return void
   *
   * @see https://www.charistheo.io/blog/2021/02/restart-a-css-animation-with-javascript/#restarting-a-css-animation
   */
  const reflow = element => {
    element.offsetHeight; // eslint-disable-line no-unused-expressions
  };
  const getjQuery = () => {
    if (window.jQuery && !document.body.hasAttribute('data-bs-no-jquery')) {
      return window.jQuery;
    }
    return null;
  };
  const DOMContentLoadedCallbacks = [];
  const onDOMContentLoaded = callback => {
    if (document.readyState === 'loading') {
      // add listener on the first call when the document is in loading state
      if (!DOMContentLoadedCallbacks.length) {
        document.addEventListener('DOMContentLoaded', () => {
          for (const callback of DOMContentLoadedCallbacks) {
            callback();
          }
        });
      }
      DOMContentLoadedCallbacks.push(callback);
    } else {
      callback();
    }
  };
  const isRTL = () => document.documentElement.dir === 'rtl';
  const defineJQueryPlugin = plugin => {
    onDOMContentLoaded(() => {
      const $ = getjQuery();
      /* istanbul ignore if */
      if ($) {
        const name = plugin.NAME;
        const JQUERY_NO_CONFLICT = $.fn[name];
        $.fn[name] = plugin.jQueryInterface;
        $.fn[name].Constructor = plugin;
        $.fn[name].noConflict = () => {
          $.fn[name] = JQUERY_NO_CONFLICT;
          return plugin.jQueryInterface;
        };
      }
    });
  };
  const execute = (possibleCallback, args = [], defaultValue = possibleCallback) => {
    return typeof possibleCallback === 'function' ? possibleCallback(...args) : defaultValue;
  };
  const executeAfterTransition = (callback, transitionElement, waitForTransition = true) => {
    if (!waitForTransition) {
      execute(callback);
      return;
    }
    const durationPadding = 5;
    const emulatedDuration = getTransitionDurationFromElement(transitionElement) + durationPadding;
    let called = false;
    const handler = ({
      target
    }) => {
      if (target !== transitionElement) {
        return;
      }
      called = true;
      transitionElement.removeEventListener(TRANSITION_END, handler);
      execute(callback);
    };
    transitionElement.addEventListener(TRANSITION_END, handler);
    setTimeout(() => {
      if (!called) {
        triggerTransitionEnd(transitionElement);
      }
    }, emulatedDuration);
  };

  /**
   * Return the previous/next element of a list.
   *
   * @param {array} list    The list of elements
   * @param activeElement   The active element
   * @param shouldGetNext   Choose to get next or previous element
   * @param isCycleAllowed
   * @return {Element|elem} The proper element
   */
  const getNextActiveElement = (list, activeElement, shouldGetNext, isCycleAllowed) => {
    const listLength = list.length;
    let index = list.indexOf(activeElement);

    // if the element does not exist in the list return an element
    // depending on the direction and if cycle is allowed
    if (index === -1) {
      return !shouldGetNext && isCycleAllowed ? list[listLength - 1] : list[0];
    }
    index += shouldGetNext ? 1 : -1;
    if (isCycleAllowed) {
      index = (index + listLength) % listLength;
    }
    return list[Math.max(0, Math.min(index, listLength - 1))];
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/event-handler.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const namespaceRegex = /[^.]*(?=\..*)\.|.*/;
  const stripNameRegex = /\..*/;
  const stripUidRegex = /::\d+$/;
  const eventRegistry = {}; // Events storage
  let uidEvent = 1;
  const customEvents = {
    mouseenter: 'mouseover',
    mouseleave: 'mouseout'
  };
  const nativeEvents = new Set(['click', 'dblclick', 'mouseup', 'mousedown', 'contextmenu', 'mousewheel', 'DOMMouseScroll', 'mouseover', 'mouseout', 'mousemove', 'selectstart', 'selectend', 'keydown', 'keypress', 'keyup', 'orientationchange', 'touchstart', 'touchmove', 'touchend', 'touchcancel', 'pointerdown', 'pointermove', 'pointerup', 'pointerleave', 'pointercancel', 'gesturestart', 'gesturechange', 'gestureend', 'focus', 'blur', 'change', 'reset', 'select', 'submit', 'focusin', 'focusout', 'load', 'unload', 'beforeunload', 'resize', 'move', 'DOMContentLoaded', 'readystatechange', 'error', 'abort', 'scroll']);

  /**
   * Private methods
   */

  function makeEventUid(element, uid) {
    return uid && `${uid}::${uidEvent++}` || element.uidEvent || uidEvent++;
  }
  function getElementEvents(element) {
    const uid = makeEventUid(element);
    element.uidEvent = uid;
    eventRegistry[uid] = eventRegistry[uid] || {};
    return eventRegistry[uid];
  }
  function bootstrapHandler(element, fn) {
    return function handler(event) {
      hydrateObj(event, {
        delegateTarget: element
      });
      if (handler.oneOff) {
        EventHandler.off(element, event.type, fn);
      }
      return fn.apply(element, [event]);
    };
  }
  function bootstrapDelegationHandler(element, selector, fn) {
    return function handler(event) {
      const domElements = element.querySelectorAll(selector);
      for (let {
        target
      } = event; target && target !== this; target = target.parentNode) {
        for (const domElement of domElements) {
          if (domElement !== target) {
            continue;
          }
          hydrateObj(event, {
            delegateTarget: target
          });
          if (handler.oneOff) {
            EventHandler.off(element, event.type, selector, fn);
          }
          return fn.apply(target, [event]);
        }
      }
    };
  }
  function findHandler(events, callable, delegationSelector = null) {
    return Object.values(events).find(event => event.callable === callable && event.delegationSelector === delegationSelector);
  }
  function normalizeParameters(originalTypeEvent, handler, delegationFunction) {
    const isDelegated = typeof handler === 'string';
    // TODO: tooltip passes `false` instead of selector, so we need to check
    const callable = isDelegated ? delegationFunction : handler || delegationFunction;
    let typeEvent = getTypeEvent(originalTypeEvent);
    if (!nativeEvents.has(typeEvent)) {
      typeEvent = originalTypeEvent;
    }
    return [isDelegated, callable, typeEvent];
  }
  function addHandler(element, originalTypeEvent, handler, delegationFunction, oneOff) {
    if (typeof originalTypeEvent !== 'string' || !element) {
      return;
    }
    let [isDelegated, callable, typeEvent] = normalizeParameters(originalTypeEvent, handler, delegationFunction);

    // in case of mouseenter or mouseleave wrap the handler within a function that checks for its DOM position
    // this prevents the handler from being dispatched the same way as mouseover or mouseout does
    if (originalTypeEvent in customEvents) {
      const wrapFunction = fn => {
        return function (event) {
          if (!event.relatedTarget || event.relatedTarget !== event.delegateTarget && !event.delegateTarget.contains(event.relatedTarget)) {
            return fn.call(this, event);
          }
        };
      };
      callable = wrapFunction(callable);
    }
    const events = getElementEvents(element);
    const handlers = events[typeEvent] || (events[typeEvent] = {});
    const previousFunction = findHandler(handlers, callable, isDelegated ? handler : null);
    if (previousFunction) {
      previousFunction.oneOff = previousFunction.oneOff && oneOff;
      return;
    }
    const uid = makeEventUid(callable, originalTypeEvent.replace(namespaceRegex, ''));
    const fn = isDelegated ? bootstrapDelegationHandler(element, handler, callable) : bootstrapHandler(element, callable);
    fn.delegationSelector = isDelegated ? handler : null;
    fn.callable = callable;
    fn.oneOff = oneOff;
    fn.uidEvent = uid;
    handlers[uid] = fn;
    element.addEventListener(typeEvent, fn, isDelegated);
  }
  function removeHandler(element, events, typeEvent, handler, delegationSelector) {
    const fn = findHandler(events[typeEvent], handler, delegationSelector);
    if (!fn) {
      return;
    }
    element.removeEventListener(typeEvent, fn, Boolean(delegationSelector));
    delete events[typeEvent][fn.uidEvent];
  }
  function removeNamespacedHandlers(element, events, typeEvent, namespace) {
    const storeElementEvent = events[typeEvent] || {};
    for (const [handlerKey, event] of Object.entries(storeElementEvent)) {
      if (handlerKey.includes(namespace)) {
        removeHandler(element, events, typeEvent, event.callable, event.delegationSelector);
      }
    }
  }
  function getTypeEvent(event) {
    // allow to get the native events from namespaced events ('click.bs.button' --> 'click')
    event = event.replace(stripNameRegex, '');
    return customEvents[event] || event;
  }
  const EventHandler = {
    on(element, event, handler, delegationFunction) {
      addHandler(element, event, handler, delegationFunction, false);
    },
    one(element, event, handler, delegationFunction) {
      addHandler(element, event, handler, delegationFunction, true);
    },
    off(element, originalTypeEvent, handler, delegationFunction) {
      if (typeof originalTypeEvent !== 'string' || !element) {
        return;
      }
      const [isDelegated, callable, typeEvent] = normalizeParameters(originalTypeEvent, handler, delegationFunction);
      const inNamespace = typeEvent !== originalTypeEvent;
      const events = getElementEvents(element);
      const storeElementEvent = events[typeEvent] || {};
      const isNamespace = originalTypeEvent.startsWith('.');
      if (typeof callable !== 'undefined') {
        // Simplest case: handler is passed, remove that listener ONLY.
        if (!Object.keys(storeElementEvent).length) {
          return;
        }
        removeHandler(element, events, typeEvent, callable, isDelegated ? handler : null);
        return;
      }
      if (isNamespace) {
        for (const elementEvent of Object.keys(events)) {
          removeNamespacedHandlers(element, events, elementEvent, originalTypeEvent.slice(1));
        }
      }
      for (const [keyHandlers, event] of Object.entries(storeElementEvent)) {
        const handlerKey = keyHandlers.replace(stripUidRegex, '');
        if (!inNamespace || originalTypeEvent.includes(handlerKey)) {
          removeHandler(element, events, typeEvent, event.callable, event.delegationSelector);
        }
      }
    },
    trigger(element, event, args) {
      if (typeof event !== 'string' || !element) {
        return null;
      }
      const $ = getjQuery();
      const typeEvent = getTypeEvent(event);
      const inNamespace = event !== typeEvent;
      let jQueryEvent = null;
      let bubbles = true;
      let nativeDispatch = true;
      let defaultPrevented = false;
      if (inNamespace && $) {
        jQueryEvent = $.Event(event, args);
        $(element).trigger(jQueryEvent);
        bubbles = !jQueryEvent.isPropagationStopped();
        nativeDispatch = !jQueryEvent.isImmediatePropagationStopped();
        defaultPrevented = jQueryEvent.isDefaultPrevented();
      }
      const evt = hydrateObj(new Event(event, {
        bubbles,
        cancelable: true
      }), args);
      if (defaultPrevented) {
        evt.preventDefault();
      }
      if (nativeDispatch) {
        element.dispatchEvent(evt);
      }
      if (evt.defaultPrevented && jQueryEvent) {
        jQueryEvent.preventDefault();
      }
      return evt;
    }
  };
  function hydrateObj(obj, meta = {}) {
    for (const [key, value] of Object.entries(meta)) {
      try {
        obj[key] = value;
      } catch (_unused) {
        Object.defineProperty(obj, key, {
          configurable: true,
          get() {
            return value;
          }
        });
      }
    }
    return obj;
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/manipulator.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  function normalizeData(value) {
    if (value === 'true') {
      return true;
    }
    if (value === 'false') {
      return false;
    }
    if (value === Number(value).toString()) {
      return Number(value);
    }
    if (value === '' || value === 'null') {
      return null;
    }
    if (typeof value !== 'string') {
      return value;
    }
    try {
      return JSON.parse(decodeURIComponent(value));
    } catch (_unused) {
      return value;
    }
  }
  function normalizeDataKey(key) {
    return key.replace(/[A-Z]/g, chr => `-${chr.toLowerCase()}`);
  }
  const Manipulator = {
    setDataAttribute(element, key, value) {
      element.setAttribute(`data-bs-${normalizeDataKey(key)}`, value);
    },
    removeDataAttribute(element, key) {
      element.removeAttribute(`data-bs-${normalizeDataKey(key)}`);
    },
    getDataAttributes(element) {
      if (!element) {
        return {};
      }
      const attributes = {};
      const bsKeys = Object.keys(element.dataset).filter(key => key.startsWith('bs') && !key.startsWith('bsConfig'));
      for (const key of bsKeys) {
        let pureKey = key.replace(/^bs/, '');
        pureKey = pureKey.charAt(0).toLowerCase() + pureKey.slice(1, pureKey.length);
        attributes[pureKey] = normalizeData(element.dataset[key]);
      }
      return attributes;
    },
    getDataAttribute(element, key) {
      return normalizeData(element.getAttribute(`data-bs-${normalizeDataKey(key)}`));
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/config.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Class definition
   */

  class Config {
    // Getters
    static get Default() {
      return {};
    }
    static get DefaultType() {
      return {};
    }
    static get NAME() {
      throw new Error('You have to implement the static method "NAME", for each component!');
    }
    _getConfig(config) {
      config = this._mergeConfigObj(config);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }
    _configAfterMerge(config) {
      return config;
    }
    _mergeConfigObj(config, element) {
      const jsonConfig = isElement$1(element) ? Manipulator.getDataAttribute(element, 'config') : {}; // try to parse

      return {
        ...this.constructor.Default,
        ...(typeof jsonConfig === 'object' ? jsonConfig : {}),
        ...(isElement$1(element) ? Manipulator.getDataAttributes(element) : {}),
        ...(typeof config === 'object' ? config : {})
      };
    }
    _typeCheckConfig(config, configTypes = this.constructor.DefaultType) {
      for (const [property, expectedTypes] of Object.entries(configTypes)) {
        const value = config[property];
        const valueType = isElement$1(value) ? 'element' : toType(value);
        if (!new RegExp(expectedTypes).test(valueType)) {
          throw new TypeError(`${this.constructor.NAME.toUpperCase()}: Option "${property}" provided type "${valueType}" but expected type "${expectedTypes}".`);
        }
      }
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap base-component.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const VERSION = '5.3.3';

  /**
   * Class definition
   */

  class BaseComponent extends Config {
    constructor(element, config) {
      super();
      element = getElement(element);
      if (!element) {
        return;
      }
      this._element = element;
      this._config = this._getConfig(config);
      Data.set(this._element, this.constructor.DATA_KEY, this);
    }

    // Public
    dispose() {
      Data.remove(this._element, this.constructor.DATA_KEY);
      EventHandler.off(this._element, this.constructor.EVENT_KEY);
      for (const propertyName of Object.getOwnPropertyNames(this)) {
        this[propertyName] = null;
      }
    }
    _queueCallback(callback, element, isAnimated = true) {
      executeAfterTransition(callback, element, isAnimated);
    }
    _getConfig(config) {
      config = this._mergeConfigObj(config, this._element);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }

    // Static
    static getInstance(element) {
      return Data.get(getElement(element), this.DATA_KEY);
    }
    static getOrCreateInstance(element, config = {}) {
      return this.getInstance(element) || new this(element, typeof config === 'object' ? config : null);
    }
    static get VERSION() {
      return VERSION;
    }
    static get DATA_KEY() {
      return `bs.${this.NAME}`;
    }
    static get EVENT_KEY() {
      return `.${this.DATA_KEY}`;
    }
    static eventName(name) {
      return `${name}${this.EVENT_KEY}`;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dom/selector-engine.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const getSelector = element => {
    let selector = element.getAttribute('data-bs-target');
    if (!selector || selector === '#') {
      let hrefAttribute = element.getAttribute('href');

      // The only valid content that could double as a selector are IDs or classes,
      // so everything starting with `#` or `.`. If a "real" URL is used as the selector,
      // `document.querySelector` will rightfully complain it is invalid.
      // See https://github.com/twbs/bootstrap/issues/32273
      if (!hrefAttribute || !hrefAttribute.includes('#') && !hrefAttribute.startsWith('.')) {
        return null;
      }

      // Just in case some CMS puts out a full URL with the anchor appended
      if (hrefAttribute.includes('#') && !hrefAttribute.startsWith('#')) {
        hrefAttribute = `#${hrefAttribute.split('#')[1]}`;
      }
      selector = hrefAttribute && hrefAttribute !== '#' ? hrefAttribute.trim() : null;
    }
    return selector ? selector.split(',').map(sel => parseSelector(sel)).join(',') : null;
  };
  const SelectorEngine = {
    find(selector, element = document.documentElement) {
      return [].concat(...Element.prototype.querySelectorAll.call(element, selector));
    },
    findOne(selector, element = document.documentElement) {
      return Element.prototype.querySelector.call(element, selector);
    },
    children(element, selector) {
      return [].concat(...element.children).filter(child => child.matches(selector));
    },
    parents(element, selector) {
      const parents = [];
      let ancestor = element.parentNode.closest(selector);
      while (ancestor) {
        parents.push(ancestor);
        ancestor = ancestor.parentNode.closest(selector);
      }
      return parents;
    },
    prev(element, selector) {
      let previous = element.previousElementSibling;
      while (previous) {
        if (previous.matches(selector)) {
          return [previous];
        }
        previous = previous.previousElementSibling;
      }
      return [];
    },
    // TODO: this is now unused; remove later along with prev()
    next(element, selector) {
      let next = element.nextElementSibling;
      while (next) {
        if (next.matches(selector)) {
          return [next];
        }
        next = next.nextElementSibling;
      }
      return [];
    },
    focusableChildren(element) {
      const focusables = ['a', 'button', 'input', 'textarea', 'select', 'details', '[tabindex]', '[contenteditable="true"]'].map(selector => `${selector}:not([tabindex^="-"])`).join(',');
      return this.find(focusables, element).filter(el => !isDisabled(el) && isVisible(el));
    },
    getSelectorFromElement(element) {
      const selector = getSelector(element);
      if (selector) {
        return SelectorEngine.findOne(selector) ? selector : null;
      }
      return null;
    },
    getElementFromSelector(element) {
      const selector = getSelector(element);
      return selector ? SelectorEngine.findOne(selector) : null;
    },
    getMultipleElementsFromSelector(element) {
      const selector = getSelector(element);
      return selector ? SelectorEngine.find(selector) : [];
    }
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/component-functions.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const enableDismissTrigger = (component, method = 'hide') => {
    const clickEvent = `click.dismiss${component.EVENT_KEY}`;
    const name = component.NAME;
    EventHandler.on(document, clickEvent, `[data-bs-dismiss="${name}"]`, function (event) {
      if (['A', 'AREA'].includes(this.tagName)) {
        event.preventDefault();
      }
      if (isDisabled(this)) {
        return;
      }
      const target = SelectorEngine.getElementFromSelector(this) || this.closest(`.${name}`);
      const instance = component.getOrCreateInstance(target);

      // Method argument is left, for Alert and only, as it doesn't implement the 'hide' method
      instance[method]();
    });
  };

  /**
   * --------------------------------------------------------------------------
   * Bootstrap alert.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$f = 'alert';
  const DATA_KEY$a = 'bs.alert';
  const EVENT_KEY$b = `.${DATA_KEY$a}`;
  const EVENT_CLOSE = `close${EVENT_KEY$b}`;
  const EVENT_CLOSED = `closed${EVENT_KEY$b}`;
  const CLASS_NAME_FADE$5 = 'fade';
  const CLASS_NAME_SHOW$8 = 'show';

  /**
   * Class definition
   */

  class Alert extends BaseComponent {
    // Getters
    static get NAME() {
      return NAME$f;
    }

    // Public
    close() {
      const closeEvent = EventHandler.trigger(this._element, EVENT_CLOSE);
      if (closeEvent.defaultPrevented) {
        return;
      }
      this._element.classList.remove(CLASS_NAME_SHOW$8);
      const isAnimated = this._element.classList.contains(CLASS_NAME_FADE$5);
      this._queueCallback(() => this._destroyElement(), this._element, isAnimated);
    }

    // Private
    _destroyElement() {
      this._element.remove();
      EventHandler.trigger(this._element, EVENT_CLOSED);
      this.dispose();
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Alert.getOrCreateInstance(this);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](this);
      });
    }
  }

  /**
   * Data API implementation
   */

  enableDismissTrigger(Alert, 'close');

  /**
   * jQuery
   */

  defineJQueryPlugin(Alert);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap button.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$e = 'button';
  const DATA_KEY$9 = 'bs.button';
  const EVENT_KEY$a = `.${DATA_KEY$9}`;
  const DATA_API_KEY$6 = '.data-api';
  const CLASS_NAME_ACTIVE$3 = 'active';
  const SELECTOR_DATA_TOGGLE$5 = '[data-bs-toggle="button"]';
  const EVENT_CLICK_DATA_API$6 = `click${EVENT_KEY$a}${DATA_API_KEY$6}`;

  /**
   * Class definition
   */

  class Button extends BaseComponent {
    // Getters
    static get NAME() {
      return NAME$e;
    }

    // Public
    toggle() {
      // Toggle class and sync the `aria-pressed` attribute with the return value of the `.toggle()` method
      this._element.setAttribute('aria-pressed', this._element.classList.toggle(CLASS_NAME_ACTIVE$3));
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Button.getOrCreateInstance(this);
        if (config === 'toggle') {
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$6, SELECTOR_DATA_TOGGLE$5, event => {
    event.preventDefault();
    const button = event.target.closest(SELECTOR_DATA_TOGGLE$5);
    const data = Button.getOrCreateInstance(button);
    data.toggle();
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Button);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/swipe.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$d = 'swipe';
  const EVENT_KEY$9 = '.bs.swipe';
  const EVENT_TOUCHSTART = `touchstart${EVENT_KEY$9}`;
  const EVENT_TOUCHMOVE = `touchmove${EVENT_KEY$9}`;
  const EVENT_TOUCHEND = `touchend${EVENT_KEY$9}`;
  const EVENT_POINTERDOWN = `pointerdown${EVENT_KEY$9}`;
  const EVENT_POINTERUP = `pointerup${EVENT_KEY$9}`;
  const POINTER_TYPE_TOUCH = 'touch';
  const POINTER_TYPE_PEN = 'pen';
  const CLASS_NAME_POINTER_EVENT = 'pointer-event';
  const SWIPE_THRESHOLD = 40;
  const Default$c = {
    endCallback: null,
    leftCallback: null,
    rightCallback: null
  };
  const DefaultType$c = {
    endCallback: '(function|null)',
    leftCallback: '(function|null)',
    rightCallback: '(function|null)'
  };

  /**
   * Class definition
   */

  class Swipe extends Config {
    constructor(element, config) {
      super();
      this._element = element;
      if (!element || !Swipe.isSupported()) {
        return;
      }
      this._config = this._getConfig(config);
      this._deltaX = 0;
      this._supportPointerEvents = Boolean(window.PointerEvent);
      this._initEvents();
    }

    // Getters
    static get Default() {
      return Default$c;
    }
    static get DefaultType() {
      return DefaultType$c;
    }
    static get NAME() {
      return NAME$d;
    }

    // Public
    dispose() {
      EventHandler.off(this._element, EVENT_KEY$9);
    }

    // Private
    _start(event) {
      if (!this._supportPointerEvents) {
        this._deltaX = event.touches[0].clientX;
        return;
      }
      if (this._eventIsPointerPenTouch(event)) {
        this._deltaX = event.clientX;
      }
    }
    _end(event) {
      if (this._eventIsPointerPenTouch(event)) {
        this._deltaX = event.clientX - this._deltaX;
      }
      this._handleSwipe();
      execute(this._config.endCallback);
    }
    _move(event) {
      this._deltaX = event.touches && event.touches.length > 1 ? 0 : event.touches[0].clientX - this._deltaX;
    }
    _handleSwipe() {
      const absDeltaX = Math.abs(this._deltaX);
      if (absDeltaX <= SWIPE_THRESHOLD) {
        return;
      }
      const direction = absDeltaX / this._deltaX;
      this._deltaX = 0;
      if (!direction) {
        return;
      }
      execute(direction > 0 ? this._config.rightCallback : this._config.leftCallback);
    }
    _initEvents() {
      if (this._supportPointerEvents) {
        EventHandler.on(this._element, EVENT_POINTERDOWN, event => this._start(event));
        EventHandler.on(this._element, EVENT_POINTERUP, event => this._end(event));
        this._element.classList.add(CLASS_NAME_POINTER_EVENT);
      } else {
        EventHandler.on(this._element, EVENT_TOUCHSTART, event => this._start(event));
        EventHandler.on(this._element, EVENT_TOUCHMOVE, event => this._move(event));
        EventHandler.on(this._element, EVENT_TOUCHEND, event => this._end(event));
      }
    }
    _eventIsPointerPenTouch(event) {
      return this._supportPointerEvents && (event.pointerType === POINTER_TYPE_PEN || event.pointerType === POINTER_TYPE_TOUCH);
    }

    // Static
    static isSupported() {
      return 'ontouchstart' in document.documentElement || navigator.maxTouchPoints > 0;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap carousel.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$c = 'carousel';
  const DATA_KEY$8 = 'bs.carousel';
  const EVENT_KEY$8 = `.${DATA_KEY$8}`;
  const DATA_API_KEY$5 = '.data-api';
  const ARROW_LEFT_KEY$1 = 'ArrowLeft';
  const ARROW_RIGHT_KEY$1 = 'ArrowRight';
  const TOUCHEVENT_COMPAT_WAIT = 500; // Time for mouse compat events to fire after touch

  const ORDER_NEXT = 'next';
  const ORDER_PREV = 'prev';
  const DIRECTION_LEFT = 'left';
  const DIRECTION_RIGHT = 'right';
  const EVENT_SLIDE = `slide${EVENT_KEY$8}`;
  const EVENT_SLID = `slid${EVENT_KEY$8}`;
  const EVENT_KEYDOWN$1 = `keydown${EVENT_KEY$8}`;
  const EVENT_MOUSEENTER$1 = `mouseenter${EVENT_KEY$8}`;
  const EVENT_MOUSELEAVE$1 = `mouseleave${EVENT_KEY$8}`;
  const EVENT_DRAG_START = `dragstart${EVENT_KEY$8}`;
  const EVENT_LOAD_DATA_API$3 = `load${EVENT_KEY$8}${DATA_API_KEY$5}`;
  const EVENT_CLICK_DATA_API$5 = `click${EVENT_KEY$8}${DATA_API_KEY$5}`;
  const CLASS_NAME_CAROUSEL = 'carousel';
  const CLASS_NAME_ACTIVE$2 = 'active';
  const CLASS_NAME_SLIDE = 'slide';
  const CLASS_NAME_END = 'carousel-item-end';
  const CLASS_NAME_START = 'carousel-item-start';
  const CLASS_NAME_NEXT = 'carousel-item-next';
  const CLASS_NAME_PREV = 'carousel-item-prev';
  const SELECTOR_ACTIVE = '.active';
  const SELECTOR_ITEM = '.carousel-item';
  const SELECTOR_ACTIVE_ITEM = SELECTOR_ACTIVE + SELECTOR_ITEM;
  const SELECTOR_ITEM_IMG = '.carousel-item img';
  const SELECTOR_INDICATORS = '.carousel-indicators';
  const SELECTOR_DATA_SLIDE = '[data-bs-slide], [data-bs-slide-to]';
  const SELECTOR_DATA_RIDE = '[data-bs-ride="carousel"]';
  const KEY_TO_DIRECTION = {
    [ARROW_LEFT_KEY$1]: DIRECTION_RIGHT,
    [ARROW_RIGHT_KEY$1]: DIRECTION_LEFT
  };
  const Default$b = {
    interval: 5000,
    keyboard: true,
    pause: 'hover',
    ride: false,
    touch: true,
    wrap: true
  };
  const DefaultType$b = {
    interval: '(number|boolean)',
    // TODO:v6 remove boolean support
    keyboard: 'boolean',
    pause: '(string|boolean)',
    ride: '(boolean|string)',
    touch: 'boolean',
    wrap: 'boolean'
  };

  /**
   * Class definition
   */

  class Carousel extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._interval = null;
      this._activeElement = null;
      this._isSliding = false;
      this.touchTimeout = null;
      this._swipeHelper = null;
      this._indicatorsElement = SelectorEngine.findOne(SELECTOR_INDICATORS, this._element);
      this._addEventListeners();
      if (this._config.ride === CLASS_NAME_CAROUSEL) {
        this.cycle();
      }
    }

    // Getters
    static get Default() {
      return Default$b;
    }
    static get DefaultType() {
      return DefaultType$b;
    }
    static get NAME() {
      return NAME$c;
    }

    // Public
    next() {
      this._slide(ORDER_NEXT);
    }
    nextWhenVisible() {
      // FIXME TODO use `document.visibilityState`
      // Don't call next when the page isn't visible
      // or the carousel or its parent isn't visible
      if (!document.hidden && isVisible(this._element)) {
        this.next();
      }
    }
    prev() {
      this._slide(ORDER_PREV);
    }
    pause() {
      if (this._isSliding) {
        triggerTransitionEnd(this._element);
      }
      this._clearInterval();
    }
    cycle() {
      this._clearInterval();
      this._updateInterval();
      this._interval = setInterval(() => this.nextWhenVisible(), this._config.interval);
    }
    _maybeEnableCycle() {
      if (!this._config.ride) {
        return;
      }
      if (this._isSliding) {
        EventHandler.one(this._element, EVENT_SLID, () => this.cycle());
        return;
      }
      this.cycle();
    }
    to(index) {
      const items = this._getItems();
      if (index > items.length - 1 || index < 0) {
        return;
      }
      if (this._isSliding) {
        EventHandler.one(this._element, EVENT_SLID, () => this.to(index));
        return;
      }
      const activeIndex = this._getItemIndex(this._getActive());
      if (activeIndex === index) {
        return;
      }
      const order = index > activeIndex ? ORDER_NEXT : ORDER_PREV;
      this._slide(order, items[index]);
    }
    dispose() {
      if (this._swipeHelper) {
        this._swipeHelper.dispose();
      }
      super.dispose();
    }

    // Private
    _configAfterMerge(config) {
      config.defaultInterval = config.interval;
      return config;
    }
    _addEventListeners() {
      if (this._config.keyboard) {
        EventHandler.on(this._element, EVENT_KEYDOWN$1, event => this._keydown(event));
      }
      if (this._config.pause === 'hover') {
        EventHandler.on(this._element, EVENT_MOUSEENTER$1, () => this.pause());
        EventHandler.on(this._element, EVENT_MOUSELEAVE$1, () => this._maybeEnableCycle());
      }
      if (this._config.touch && Swipe.isSupported()) {
        this._addTouchEventListeners();
      }
    }
    _addTouchEventListeners() {
      for (const img of SelectorEngine.find(SELECTOR_ITEM_IMG, this._element)) {
        EventHandler.on(img, EVENT_DRAG_START, event => event.preventDefault());
      }
      const endCallBack = () => {
        if (this._config.pause !== 'hover') {
          return;
        }

        // If it's a touch-enabled device, mouseenter/leave are fired as
        // part of the mouse compatibility events on first tap - the carousel
        // would stop cycling until user tapped out of it;
        // here, we listen for touchend, explicitly pause the carousel
        // (as if it's the second time we tap on it, mouseenter compat event
        // is NOT fired) and after a timeout (to allow for mouse compatibility
        // events to fire) we explicitly restart cycling

        this.pause();
        if (this.touchTimeout) {
          clearTimeout(this.touchTimeout);
        }
        this.touchTimeout = setTimeout(() => this._maybeEnableCycle(), TOUCHEVENT_COMPAT_WAIT + this._config.interval);
      };
      const swipeConfig = {
        leftCallback: () => this._slide(this._directionToOrder(DIRECTION_LEFT)),
        rightCallback: () => this._slide(this._directionToOrder(DIRECTION_RIGHT)),
        endCallback: endCallBack
      };
      this._swipeHelper = new Swipe(this._element, swipeConfig);
    }
    _keydown(event) {
      if (/input|textarea/i.test(event.target.tagName)) {
        return;
      }
      const direction = KEY_TO_DIRECTION[event.key];
      if (direction) {
        event.preventDefault();
        this._slide(this._directionToOrder(direction));
      }
    }
    _getItemIndex(element) {
      return this._getItems().indexOf(element);
    }
    _setActiveIndicatorElement(index) {
      if (!this._indicatorsElement) {
        return;
      }
      const activeIndicator = SelectorEngine.findOne(SELECTOR_ACTIVE, this._indicatorsElement);
      activeIndicator.classList.remove(CLASS_NAME_ACTIVE$2);
      activeIndicator.removeAttribute('aria-current');
      const newActiveIndicator = SelectorEngine.findOne(`[data-bs-slide-to="${index}"]`, this._indicatorsElement);
      if (newActiveIndicator) {
        newActiveIndicator.classList.add(CLASS_NAME_ACTIVE$2);
        newActiveIndicator.setAttribute('aria-current', 'true');
      }
    }
    _updateInterval() {
      const element = this._activeElement || this._getActive();
      if (!element) {
        return;
      }
      const elementInterval = Number.parseInt(element.getAttribute('data-bs-interval'), 10);
      this._config.interval = elementInterval || this._config.defaultInterval;
    }
    _slide(order, element = null) {
      if (this._isSliding) {
        return;
      }
      const activeElement = this._getActive();
      const isNext = order === ORDER_NEXT;
      const nextElement = element || getNextActiveElement(this._getItems(), activeElement, isNext, this._config.wrap);
      if (nextElement === activeElement) {
        return;
      }
      const nextElementIndex = this._getItemIndex(nextElement);
      const triggerEvent = eventName => {
        return EventHandler.trigger(this._element, eventName, {
          relatedTarget: nextElement,
          direction: this._orderToDirection(order),
          from: this._getItemIndex(activeElement),
          to: nextElementIndex
        });
      };
      const slideEvent = triggerEvent(EVENT_SLIDE);
      if (slideEvent.defaultPrevented) {
        return;
      }
      if (!activeElement || !nextElement) {
        // Some weirdness is happening, so we bail
        // TODO: change tests that use empty divs to avoid this check
        return;
      }
      const isCycling = Boolean(this._interval);
      this.pause();
      this._isSliding = true;
      this._setActiveIndicatorElement(nextElementIndex);
      this._activeElement = nextElement;
      const directionalClassName = isNext ? CLASS_NAME_START : CLASS_NAME_END;
      const orderClassName = isNext ? CLASS_NAME_NEXT : CLASS_NAME_PREV;
      nextElement.classList.add(orderClassName);
      reflow(nextElement);
      activeElement.classList.add(directionalClassName);
      nextElement.classList.add(directionalClassName);
      const completeCallBack = () => {
        nextElement.classList.remove(directionalClassName, orderClassName);
        nextElement.classList.add(CLASS_NAME_ACTIVE$2);
        activeElement.classList.remove(CLASS_NAME_ACTIVE$2, orderClassName, directionalClassName);
        this._isSliding = false;
        triggerEvent(EVENT_SLID);
      };
      this._queueCallback(completeCallBack, activeElement, this._isAnimated());
      if (isCycling) {
        this.cycle();
      }
    }
    _isAnimated() {
      return this._element.classList.contains(CLASS_NAME_SLIDE);
    }
    _getActive() {
      return SelectorEngine.findOne(SELECTOR_ACTIVE_ITEM, this._element);
    }
    _getItems() {
      return SelectorEngine.find(SELECTOR_ITEM, this._element);
    }
    _clearInterval() {
      if (this._interval) {
        clearInterval(this._interval);
        this._interval = null;
      }
    }
    _directionToOrder(direction) {
      if (isRTL()) {
        return direction === DIRECTION_LEFT ? ORDER_PREV : ORDER_NEXT;
      }
      return direction === DIRECTION_LEFT ? ORDER_NEXT : ORDER_PREV;
    }
    _orderToDirection(order) {
      if (isRTL()) {
        return order === ORDER_PREV ? DIRECTION_LEFT : DIRECTION_RIGHT;
      }
      return order === ORDER_PREV ? DIRECTION_RIGHT : DIRECTION_LEFT;
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Carousel.getOrCreateInstance(this, config);
        if (typeof config === 'number') {
          data.to(config);
          return;
        }
        if (typeof config === 'string') {
          if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$5, SELECTOR_DATA_SLIDE, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (!target || !target.classList.contains(CLASS_NAME_CAROUSEL)) {
      return;
    }
    event.preventDefault();
    const carousel = Carousel.getOrCreateInstance(target);
    const slideIndex = this.getAttribute('data-bs-slide-to');
    if (slideIndex) {
      carousel.to(slideIndex);
      carousel._maybeEnableCycle();
      return;
    }
    if (Manipulator.getDataAttribute(this, 'slide') === 'next') {
      carousel.next();
      carousel._maybeEnableCycle();
      return;
    }
    carousel.prev();
    carousel._maybeEnableCycle();
  });
  EventHandler.on(window, EVENT_LOAD_DATA_API$3, () => {
    const carousels = SelectorEngine.find(SELECTOR_DATA_RIDE);
    for (const carousel of carousels) {
      Carousel.getOrCreateInstance(carousel);
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Carousel);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap collapse.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$b = 'collapse';
  const DATA_KEY$7 = 'bs.collapse';
  const EVENT_KEY$7 = `.${DATA_KEY$7}`;
  const DATA_API_KEY$4 = '.data-api';
  const EVENT_SHOW$6 = `show${EVENT_KEY$7}`;
  const EVENT_SHOWN$6 = `shown${EVENT_KEY$7}`;
  const EVENT_HIDE$6 = `hide${EVENT_KEY$7}`;
  const EVENT_HIDDEN$6 = `hidden${EVENT_KEY$7}`;
  const EVENT_CLICK_DATA_API$4 = `click${EVENT_KEY$7}${DATA_API_KEY$4}`;
  const CLASS_NAME_SHOW$7 = 'show';
  const CLASS_NAME_COLLAPSE = 'collapse';
  const CLASS_NAME_COLLAPSING = 'collapsing';
  const CLASS_NAME_COLLAPSED = 'collapsed';
  const CLASS_NAME_DEEPER_CHILDREN = `:scope .${CLASS_NAME_COLLAPSE} .${CLASS_NAME_COLLAPSE}`;
  const CLASS_NAME_HORIZONTAL = 'collapse-horizontal';
  const WIDTH = 'width';
  const HEIGHT = 'height';
  const SELECTOR_ACTIVES = '.collapse.show, .collapse.collapsing';
  const SELECTOR_DATA_TOGGLE$4 = '[data-bs-toggle="collapse"]';
  const Default$a = {
    parent: null,
    toggle: true
  };
  const DefaultType$a = {
    parent: '(null|element)',
    toggle: 'boolean'
  };

  /**
   * Class definition
   */

  class Collapse extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._isTransitioning = false;
      this._triggerArray = [];
      const toggleList = SelectorEngine.find(SELECTOR_DATA_TOGGLE$4);
      for (const elem of toggleList) {
        const selector = SelectorEngine.getSelectorFromElement(elem);
        const filterElement = SelectorEngine.find(selector).filter(foundElement => foundElement === this._element);
        if (selector !== null && filterElement.length) {
          this._triggerArray.push(elem);
        }
      }
      this._initializeChildren();
      if (!this._config.parent) {
        this._addAriaAndCollapsedClass(this._triggerArray, this._isShown());
      }
      if (this._config.toggle) {
        this.toggle();
      }
    }

    // Getters
    static get Default() {
      return Default$a;
    }
    static get DefaultType() {
      return DefaultType$a;
    }
    static get NAME() {
      return NAME$b;
    }

    // Public
    toggle() {
      if (this._isShown()) {
        this.hide();
      } else {
        this.show();
      }
    }
    show() {
      if (this._isTransitioning || this._isShown()) {
        return;
      }
      let activeChildren = [];

      // find active children
      if (this._config.parent) {
        activeChildren = this._getFirstLevelChildren(SELECTOR_ACTIVES).filter(element => element !== this._element).map(element => Collapse.getOrCreateInstance(element, {
          toggle: false
        }));
      }
      if (activeChildren.length && activeChildren[0]._isTransitioning) {
        return;
      }
      const startEvent = EventHandler.trigger(this._element, EVENT_SHOW$6);
      if (startEvent.defaultPrevented) {
        return;
      }
      for (const activeInstance of activeChildren) {
        activeInstance.hide();
      }
      const dimension = this._getDimension();
      this._element.classList.remove(CLASS_NAME_COLLAPSE);
      this._element.classList.add(CLASS_NAME_COLLAPSING);
      this._element.style[dimension] = 0;
      this._addAriaAndCollapsedClass(this._triggerArray, true);
      this._isTransitioning = true;
      const complete = () => {
        this._isTransitioning = false;
        this._element.classList.remove(CLASS_NAME_COLLAPSING);
        this._element.classList.add(CLASS_NAME_COLLAPSE, CLASS_NAME_SHOW$7);
        this._element.style[dimension] = '';
        EventHandler.trigger(this._element, EVENT_SHOWN$6);
      };
      const capitalizedDimension = dimension[0].toUpperCase() + dimension.slice(1);
      const scrollSize = `scroll${capitalizedDimension}`;
      this._queueCallback(complete, this._element, true);
      this._element.style[dimension] = `${this._element[scrollSize]}px`;
    }
    hide() {
      if (this._isTransitioning || !this._isShown()) {
        return;
      }
      const startEvent = EventHandler.trigger(this._element, EVENT_HIDE$6);
      if (startEvent.defaultPrevented) {
        return;
      }
      const dimension = this._getDimension();
      this._element.style[dimension] = `${this._element.getBoundingClientRect()[dimension]}px`;
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_COLLAPSING);
      this._element.classList.remove(CLASS_NAME_COLLAPSE, CLASS_NAME_SHOW$7);
      for (const trigger of this._triggerArray) {
        const element = SelectorEngine.getElementFromSelector(trigger);
        if (element && !this._isShown(element)) {
          this._addAriaAndCollapsedClass([trigger], false);
        }
      }
      this._isTransitioning = true;
      const complete = () => {
        this._isTransitioning = false;
        this._element.classList.remove(CLASS_NAME_COLLAPSING);
        this._element.classList.add(CLASS_NAME_COLLAPSE);
        EventHandler.trigger(this._element, EVENT_HIDDEN$6);
      };
      this._element.style[dimension] = '';
      this._queueCallback(complete, this._element, true);
    }
    _isShown(element = this._element) {
      return element.classList.contains(CLASS_NAME_SHOW$7);
    }

    // Private
    _configAfterMerge(config) {
      config.toggle = Boolean(config.toggle); // Coerce string values
      config.parent = getElement(config.parent);
      return config;
    }
    _getDimension() {
      return this._element.classList.contains(CLASS_NAME_HORIZONTAL) ? WIDTH : HEIGHT;
    }
    _initializeChildren() {
      if (!this._config.parent) {
        return;
      }
      const children = this._getFirstLevelChildren(SELECTOR_DATA_TOGGLE$4);
      for (const element of children) {
        const selected = SelectorEngine.getElementFromSelector(element);
        if (selected) {
          this._addAriaAndCollapsedClass([element], this._isShown(selected));
        }
      }
    }
    _getFirstLevelChildren(selector) {
      const children = SelectorEngine.find(CLASS_NAME_DEEPER_CHILDREN, this._config.parent);
      // remove children if greater depth
      return SelectorEngine.find(selector, this._config.parent).filter(element => !children.includes(element));
    }
    _addAriaAndCollapsedClass(triggerArray, isOpen) {
      if (!triggerArray.length) {
        return;
      }
      for (const element of triggerArray) {
        element.classList.toggle(CLASS_NAME_COLLAPSED, !isOpen);
        element.setAttribute('aria-expanded', isOpen);
      }
    }

    // Static
    static jQueryInterface(config) {
      const _config = {};
      if (typeof config === 'string' && /show|hide/.test(config)) {
        _config.toggle = false;
      }
      return this.each(function () {
        const data = Collapse.getOrCreateInstance(this, _config);
        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config]();
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$4, SELECTOR_DATA_TOGGLE$4, function (event) {
    // preventDefault only for <a> elements (which change the URL) not inside the collapsible element
    if (event.target.tagName === 'A' || event.delegateTarget && event.delegateTarget.tagName === 'A') {
      event.preventDefault();
    }
    for (const element of SelectorEngine.getMultipleElementsFromSelector(this)) {
      Collapse.getOrCreateInstance(element, {
        toggle: false
      }).toggle();
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Collapse);

  var top = 'top';
  var bottom = 'bottom';
  var right = 'right';
  var left = 'left';
  var auto = 'auto';
  var basePlacements = [top, bottom, right, left];
  var start = 'start';
  var end = 'end';
  var clippingParents = 'clippingParents';
  var viewport = 'viewport';
  var popper = 'popper';
  var reference = 'reference';
  var variationPlacements = /*#__PURE__*/basePlacements.reduce(function (acc, placement) {
    return acc.concat([placement + "-" + start, placement + "-" + end]);
  }, []);
  var placements = /*#__PURE__*/[].concat(basePlacements, [auto]).reduce(function (acc, placement) {
    return acc.concat([placement, placement + "-" + start, placement + "-" + end]);
  }, []); // modifiers that need to read the DOM

  var beforeRead = 'beforeRead';
  var read = 'read';
  var afterRead = 'afterRead'; // pure-logic modifiers

  var beforeMain = 'beforeMain';
  var main = 'main';
  var afterMain = 'afterMain'; // modifier with the purpose to write to the DOM (or write into a framework state)

  var beforeWrite = 'beforeWrite';
  var write = 'write';
  var afterWrite = 'afterWrite';
  var modifierPhases = [beforeRead, read, afterRead, beforeMain, main, afterMain, beforeWrite, write, afterWrite];

  function getNodeName(element) {
    return element ? (element.nodeName || '').toLowerCase() : null;
  }

  function getWindow(node) {
    if (node == null) {
      return window;
    }

    if (node.toString() !== '[object Window]') {
      var ownerDocument = node.ownerDocument;
      return ownerDocument ? ownerDocument.defaultView || window : window;
    }

    return node;
  }

  function isElement(node) {
    var OwnElement = getWindow(node).Element;
    return node instanceof OwnElement || node instanceof Element;
  }

  function isHTMLElement(node) {
    var OwnElement = getWindow(node).HTMLElement;
    return node instanceof OwnElement || node instanceof HTMLElement;
  }

  function isShadowRoot(node) {
    // IE 11 has no ShadowRoot
    if (typeof ShadowRoot === 'undefined') {
      return false;
    }

    var OwnElement = getWindow(node).ShadowRoot;
    return node instanceof OwnElement || node instanceof ShadowRoot;
  }

  // and applies them to the HTMLElements such as popper and arrow

  function applyStyles(_ref) {
    var state = _ref.state;
    Object.keys(state.elements).forEach(function (name) {
      var style = state.styles[name] || {};
      var attributes = state.attributes[name] || {};
      var element = state.elements[name]; // arrow is optional + virtual elements

      if (!isHTMLElement(element) || !getNodeName(element)) {
        return;
      } // Flow doesn't support to extend this property, but it's the most
      // effective way to apply styles to an HTMLElement
      // $FlowFixMe[cannot-write]


      Object.assign(element.style, style);
      Object.keys(attributes).forEach(function (name) {
        var value = attributes[name];

        if (value === false) {
          element.removeAttribute(name);
        } else {
          element.setAttribute(name, value === true ? '' : value);
        }
      });
    });
  }

  function effect$2(_ref2) {
    var state = _ref2.state;
    var initialStyles = {
      popper: {
        position: state.options.strategy,
        left: '0',
        top: '0',
        margin: '0'
      },
      arrow: {
        position: 'absolute'
      },
      reference: {}
    };
    Object.assign(state.elements.popper.style, initialStyles.popper);
    state.styles = initialStyles;

    if (state.elements.arrow) {
      Object.assign(state.elements.arrow.style, initialStyles.arrow);
    }

    return function () {
      Object.keys(state.elements).forEach(function (name) {
        var element = state.elements[name];
        var attributes = state.attributes[name] || {};
        var styleProperties = Object.keys(state.styles.hasOwnProperty(name) ? state.styles[name] : initialStyles[name]); // Set all values to an empty string to unset them

        var style = styleProperties.reduce(function (style, property) {
          style[property] = '';
          return style;
        }, {}); // arrow is optional + virtual elements

        if (!isHTMLElement(element) || !getNodeName(element)) {
          return;
        }

        Object.assign(element.style, style);
        Object.keys(attributes).forEach(function (attribute) {
          element.removeAttribute(attribute);
        });
      });
    };
  } // eslint-disable-next-line import/no-unused-modules


  const applyStyles$1 = {
    name: 'applyStyles',
    enabled: true,
    phase: 'write',
    fn: applyStyles,
    effect: effect$2,
    requires: ['computeStyles']
  };

  function getBasePlacement(placement) {
    return placement.split('-')[0];
  }

  var max = Math.max;
  var min = Math.min;
  var round = Math.round;

  function getUAString() {
    var uaData = navigator.userAgentData;

    if (uaData != null && uaData.brands && Array.isArray(uaData.brands)) {
      return uaData.brands.map(function (item) {
        return item.brand + "/" + item.version;
      }).join(' ');
    }

    return navigator.userAgent;
  }

  function isLayoutViewport() {
    return !/^((?!chrome|android).)*safari/i.test(getUAString());
  }

  function getBoundingClientRect(element, includeScale, isFixedStrategy) {
    if (includeScale === void 0) {
      includeScale = false;
    }

    if (isFixedStrategy === void 0) {
      isFixedStrategy = false;
    }

    var clientRect = element.getBoundingClientRect();
    var scaleX = 1;
    var scaleY = 1;

    if (includeScale && isHTMLElement(element)) {
      scaleX = element.offsetWidth > 0 ? round(clientRect.width) / element.offsetWidth || 1 : 1;
      scaleY = element.offsetHeight > 0 ? round(clientRect.height) / element.offsetHeight || 1 : 1;
    }

    var _ref = isElement(element) ? getWindow(element) : window,
        visualViewport = _ref.visualViewport;

    var addVisualOffsets = !isLayoutViewport() && isFixedStrategy;
    var x = (clientRect.left + (addVisualOffsets && visualViewport ? visualViewport.offsetLeft : 0)) / scaleX;
    var y = (clientRect.top + (addVisualOffsets && visualViewport ? visualViewport.offsetTop : 0)) / scaleY;
    var width = clientRect.width / scaleX;
    var height = clientRect.height / scaleY;
    return {
      width: width,
      height: height,
      top: y,
      right: x + width,
      bottom: y + height,
      left: x,
      x: x,
      y: y
    };
  }

  // means it doesn't take into account transforms.

  function getLayoutRect(element) {
    var clientRect = getBoundingClientRect(element); // Use the clientRect sizes if it's not been transformed.
    // Fixes https://github.com/popperjs/popper-core/issues/1223

    var width = element.offsetWidth;
    var height = element.offsetHeight;

    if (Math.abs(clientRect.width - width) <= 1) {
      width = clientRect.width;
    }

    if (Math.abs(clientRect.height - height) <= 1) {
      height = clientRect.height;
    }

    return {
      x: element.offsetLeft,
      y: element.offsetTop,
      width: width,
      height: height
    };
  }

  function contains(parent, child) {
    var rootNode = child.getRootNode && child.getRootNode(); // First, attempt with faster native method

    if (parent.contains(child)) {
      return true;
    } // then fallback to custom implementation with Shadow DOM support
    else if (rootNode && isShadowRoot(rootNode)) {
        var next = child;

        do {
          if (next && parent.isSameNode(next)) {
            return true;
          } // $FlowFixMe[prop-missing]: need a better way to handle this...


          next = next.parentNode || next.host;
        } while (next);
      } // Give up, the result is false


    return false;
  }

  function getComputedStyle$1(element) {
    return getWindow(element).getComputedStyle(element);
  }

  function isTableElement(element) {
    return ['table', 'td', 'th'].indexOf(getNodeName(element)) >= 0;
  }

  function getDocumentElement(element) {
    // $FlowFixMe[incompatible-return]: assume body is always available
    return ((isElement(element) ? element.ownerDocument : // $FlowFixMe[prop-missing]
    element.document) || window.document).documentElement;
  }

  function getParentNode(element) {
    if (getNodeName(element) === 'html') {
      return element;
    }

    return (// this is a quicker (but less type safe) way to save quite some bytes from the bundle
      // $FlowFixMe[incompatible-return]
      // $FlowFixMe[prop-missing]
      element.assignedSlot || // step into the shadow DOM of the parent of a slotted node
      element.parentNode || ( // DOM Element detected
      isShadowRoot(element) ? element.host : null) || // ShadowRoot detected
      // $FlowFixMe[incompatible-call]: HTMLElement is a Node
      getDocumentElement(element) // fallback

    );
  }

  function getTrueOffsetParent(element) {
    if (!isHTMLElement(element) || // https://github.com/popperjs/popper-core/issues/837
    getComputedStyle$1(element).position === 'fixed') {
      return null;
    }

    return element.offsetParent;
  } // `.offsetParent` reports `null` for fixed elements, while absolute elements
  // return the containing block


  function getContainingBlock(element) {
    var isFirefox = /firefox/i.test(getUAString());
    var isIE = /Trident/i.test(getUAString());

    if (isIE && isHTMLElement(element)) {
      // In IE 9, 10 and 11 fixed elements containing block is always established by the viewport
      var elementCss = getComputedStyle$1(element);

      if (elementCss.position === 'fixed') {
        return null;
      }
    }

    var currentNode = getParentNode(element);

    if (isShadowRoot(currentNode)) {
      currentNode = currentNode.host;
    }

    while (isHTMLElement(currentNode) && ['html', 'body'].indexOf(getNodeName(currentNode)) < 0) {
      var css = getComputedStyle$1(currentNode); // This is non-exhaustive but covers the most common CSS properties that
      // create a containing block.
      // https://developer.mozilla.org/en-US/docs/Web/CSS/Containing_block#identifying_the_containing_block

      if (css.transform !== 'none' || css.perspective !== 'none' || css.contain === 'paint' || ['transform', 'perspective'].indexOf(css.willChange) !== -1 || isFirefox && css.willChange === 'filter' || isFirefox && css.filter && css.filter !== 'none') {
        return currentNode;
      } else {
        currentNode = currentNode.parentNode;
      }
    }

    return null;
  } // Gets the closest ancestor positioned element. Handles some edge cases,
  // such as table ancestors and cross browser bugs.


  function getOffsetParent(element) {
    var window = getWindow(element);
    var offsetParent = getTrueOffsetParent(element);

    while (offsetParent && isTableElement(offsetParent) && getComputedStyle$1(offsetParent).position === 'static') {
      offsetParent = getTrueOffsetParent(offsetParent);
    }

    if (offsetParent && (getNodeName(offsetParent) === 'html' || getNodeName(offsetParent) === 'body' && getComputedStyle$1(offsetParent).position === 'static')) {
      return window;
    }

    return offsetParent || getContainingBlock(element) || window;
  }

  function getMainAxisFromPlacement(placement) {
    return ['top', 'bottom'].indexOf(placement) >= 0 ? 'x' : 'y';
  }

  function within(min$1, value, max$1) {
    return max(min$1, min(value, max$1));
  }
  function withinMaxClamp(min, value, max) {
    var v = within(min, value, max);
    return v > max ? max : v;
  }

  function getFreshSideObject() {
    return {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    };
  }

  function mergePaddingObject(paddingObject) {
    return Object.assign({}, getFreshSideObject(), paddingObject);
  }

  function expandToHashMap(value, keys) {
    return keys.reduce(function (hashMap, key) {
      hashMap[key] = value;
      return hashMap;
    }, {});
  }

  var toPaddingObject = function toPaddingObject(padding, state) {
    padding = typeof padding === 'function' ? padding(Object.assign({}, state.rects, {
      placement: state.placement
    })) : padding;
    return mergePaddingObject(typeof padding !== 'number' ? padding : expandToHashMap(padding, basePlacements));
  };

  function arrow(_ref) {
    var _state$modifiersData$;

    var state = _ref.state,
        name = _ref.name,
        options = _ref.options;
    var arrowElement = state.elements.arrow;
    var popperOffsets = state.modifiersData.popperOffsets;
    var basePlacement = getBasePlacement(state.placement);
    var axis = getMainAxisFromPlacement(basePlacement);
    var isVertical = [left, right].indexOf(basePlacement) >= 0;
    var len = isVertical ? 'height' : 'width';

    if (!arrowElement || !popperOffsets) {
      return;
    }

    var paddingObject = toPaddingObject(options.padding, state);
    var arrowRect = getLayoutRect(arrowElement);
    var minProp = axis === 'y' ? top : left;
    var maxProp = axis === 'y' ? bottom : right;
    var endDiff = state.rects.reference[len] + state.rects.reference[axis] - popperOffsets[axis] - state.rects.popper[len];
    var startDiff = popperOffsets[axis] - state.rects.reference[axis];
    var arrowOffsetParent = getOffsetParent(arrowElement);
    var clientSize = arrowOffsetParent ? axis === 'y' ? arrowOffsetParent.clientHeight || 0 : arrowOffsetParent.clientWidth || 0 : 0;
    var centerToReference = endDiff / 2 - startDiff / 2; // Make sure the arrow doesn't overflow the popper if the center point is
    // outside of the popper bounds

    var min = paddingObject[minProp];
    var max = clientSize - arrowRect[len] - paddingObject[maxProp];
    var center = clientSize / 2 - arrowRect[len] / 2 + centerToReference;
    var offset = within(min, center, max); // Prevents breaking syntax highlighting...

    var axisProp = axis;
    state.modifiersData[name] = (_state$modifiersData$ = {}, _state$modifiersData$[axisProp] = offset, _state$modifiersData$.centerOffset = offset - center, _state$modifiersData$);
  }

  function effect$1(_ref2) {
    var state = _ref2.state,
        options = _ref2.options;
    var _options$element = options.element,
        arrowElement = _options$element === void 0 ? '[data-popper-arrow]' : _options$element;

    if (arrowElement == null) {
      return;
    } // CSS selector


    if (typeof arrowElement === 'string') {
      arrowElement = state.elements.popper.querySelector(arrowElement);

      if (!arrowElement) {
        return;
      }
    }

    if (!contains(state.elements.popper, arrowElement)) {
      return;
    }

    state.elements.arrow = arrowElement;
  } // eslint-disable-next-line import/no-unused-modules


  const arrow$1 = {
    name: 'arrow',
    enabled: true,
    phase: 'main',
    fn: arrow,
    effect: effect$1,
    requires: ['popperOffsets'],
    requiresIfExists: ['preventOverflow']
  };

  function getVariation(placement) {
    return placement.split('-')[1];
  }

  var unsetSides = {
    top: 'auto',
    right: 'auto',
    bottom: 'auto',
    left: 'auto'
  }; // Round the offsets to the nearest suitable subpixel based on the DPR.
  // Zooming can change the DPR, but it seems to report a value that will
  // cleanly divide the values into the appropriate subpixels.

  function roundOffsetsByDPR(_ref, win) {
    var x = _ref.x,
        y = _ref.y;
    var dpr = win.devicePixelRatio || 1;
    return {
      x: round(x * dpr) / dpr || 0,
      y: round(y * dpr) / dpr || 0
    };
  }

  function mapToStyles(_ref2) {
    var _Object$assign2;

    var popper = _ref2.popper,
        popperRect = _ref2.popperRect,
        placement = _ref2.placement,
        variation = _ref2.variation,
        offsets = _ref2.offsets,
        position = _ref2.position,
        gpuAcceleration = _ref2.gpuAcceleration,
        adaptive = _ref2.adaptive,
        roundOffsets = _ref2.roundOffsets,
        isFixed = _ref2.isFixed;
    var _offsets$x = offsets.x,
        x = _offsets$x === void 0 ? 0 : _offsets$x,
        _offsets$y = offsets.y,
        y = _offsets$y === void 0 ? 0 : _offsets$y;

    var _ref3 = typeof roundOffsets === 'function' ? roundOffsets({
      x: x,
      y: y
    }) : {
      x: x,
      y: y
    };

    x = _ref3.x;
    y = _ref3.y;
    var hasX = offsets.hasOwnProperty('x');
    var hasY = offsets.hasOwnProperty('y');
    var sideX = left;
    var sideY = top;
    var win = window;

    if (adaptive) {
      var offsetParent = getOffsetParent(popper);
      var heightProp = 'clientHeight';
      var widthProp = 'clientWidth';

      if (offsetParent === getWindow(popper)) {
        offsetParent = getDocumentElement(popper);

        if (getComputedStyle$1(offsetParent).position !== 'static' && position === 'absolute') {
          heightProp = 'scrollHeight';
          widthProp = 'scrollWidth';
        }
      } // $FlowFixMe[incompatible-cast]: force type refinement, we compare offsetParent with window above, but Flow doesn't detect it


      offsetParent = offsetParent;

      if (placement === top || (placement === left || placement === right) && variation === end) {
        sideY = bottom;
        var offsetY = isFixed && offsetParent === win && win.visualViewport ? win.visualViewport.height : // $FlowFixMe[prop-missing]
        offsetParent[heightProp];
        y -= offsetY - popperRect.height;
        y *= gpuAcceleration ? 1 : -1;
      }

      if (placement === left || (placement === top || placement === bottom) && variation === end) {
        sideX = right;
        var offsetX = isFixed && offsetParent === win && win.visualViewport ? win.visualViewport.width : // $FlowFixMe[prop-missing]
        offsetParent[widthProp];
        x -= offsetX - popperRect.width;
        x *= gpuAcceleration ? 1 : -1;
      }
    }

    var commonStyles = Object.assign({
      position: position
    }, adaptive && unsetSides);

    var _ref4 = roundOffsets === true ? roundOffsetsByDPR({
      x: x,
      y: y
    }, getWindow(popper)) : {
      x: x,
      y: y
    };

    x = _ref4.x;
    y = _ref4.y;

    if (gpuAcceleration) {
      var _Object$assign;

      return Object.assign({}, commonStyles, (_Object$assign = {}, _Object$assign[sideY] = hasY ? '0' : '', _Object$assign[sideX] = hasX ? '0' : '', _Object$assign.transform = (win.devicePixelRatio || 1) <= 1 ? "translate(" + x + "px, " + y + "px)" : "translate3d(" + x + "px, " + y + "px, 0)", _Object$assign));
    }

    return Object.assign({}, commonStyles, (_Object$assign2 = {}, _Object$assign2[sideY] = hasY ? y + "px" : '', _Object$assign2[sideX] = hasX ? x + "px" : '', _Object$assign2.transform = '', _Object$assign2));
  }

  function computeStyles(_ref5) {
    var state = _ref5.state,
        options = _ref5.options;
    var _options$gpuAccelerat = options.gpuAcceleration,
        gpuAcceleration = _options$gpuAccelerat === void 0 ? true : _options$gpuAccelerat,
        _options$adaptive = options.adaptive,
        adaptive = _options$adaptive === void 0 ? true : _options$adaptive,
        _options$roundOffsets = options.roundOffsets,
        roundOffsets = _options$roundOffsets === void 0 ? true : _options$roundOffsets;
    var commonStyles = {
      placement: getBasePlacement(state.placement),
      variation: getVariation(state.placement),
      popper: state.elements.popper,
      popperRect: state.rects.popper,
      gpuAcceleration: gpuAcceleration,
      isFixed: state.options.strategy === 'fixed'
    };

    if (state.modifiersData.popperOffsets != null) {
      state.styles.popper = Object.assign({}, state.styles.popper, mapToStyles(Object.assign({}, commonStyles, {
        offsets: state.modifiersData.popperOffsets,
        position: state.options.strategy,
        adaptive: adaptive,
        roundOffsets: roundOffsets
      })));
    }

    if (state.modifiersData.arrow != null) {
      state.styles.arrow = Object.assign({}, state.styles.arrow, mapToStyles(Object.assign({}, commonStyles, {
        offsets: state.modifiersData.arrow,
        position: 'absolute',
        adaptive: false,
        roundOffsets: roundOffsets
      })));
    }

    state.attributes.popper = Object.assign({}, state.attributes.popper, {
      'data-popper-placement': state.placement
    });
  } // eslint-disable-next-line import/no-unused-modules


  const computeStyles$1 = {
    name: 'computeStyles',
    enabled: true,
    phase: 'beforeWrite',
    fn: computeStyles,
    data: {}
  };

  var passive = {
    passive: true
  };

  function effect(_ref) {
    var state = _ref.state,
        instance = _ref.instance,
        options = _ref.options;
    var _options$scroll = options.scroll,
        scroll = _options$scroll === void 0 ? true : _options$scroll,
        _options$resize = options.resize,
        resize = _options$resize === void 0 ? true : _options$resize;
    var window = getWindow(state.elements.popper);
    var scrollParents = [].concat(state.scrollParents.reference, state.scrollParents.popper);

    if (scroll) {
      scrollParents.forEach(function (scrollParent) {
        scrollParent.addEventListener('scroll', instance.update, passive);
      });
    }

    if (resize) {
      window.addEventListener('resize', instance.update, passive);
    }

    return function () {
      if (scroll) {
        scrollParents.forEach(function (scrollParent) {
          scrollParent.removeEventListener('scroll', instance.update, passive);
        });
      }

      if (resize) {
        window.removeEventListener('resize', instance.update, passive);
      }
    };
  } // eslint-disable-next-line import/no-unused-modules


  const eventListeners = {
    name: 'eventListeners',
    enabled: true,
    phase: 'write',
    fn: function fn() {},
    effect: effect,
    data: {}
  };

  var hash$1 = {
    left: 'right',
    right: 'left',
    bottom: 'top',
    top: 'bottom'
  };
  function getOppositePlacement(placement) {
    return placement.replace(/left|right|bottom|top/g, function (matched) {
      return hash$1[matched];
    });
  }

  var hash = {
    start: 'end',
    end: 'start'
  };
  function getOppositeVariationPlacement(placement) {
    return placement.replace(/start|end/g, function (matched) {
      return hash[matched];
    });
  }

  function getWindowScroll(node) {
    var win = getWindow(node);
    var scrollLeft = win.pageXOffset;
    var scrollTop = win.pageYOffset;
    return {
      scrollLeft: scrollLeft,
      scrollTop: scrollTop
    };
  }

  function getWindowScrollBarX(element) {
    // If <html> has a CSS width greater than the viewport, then this will be
    // incorrect for RTL.
    // Popper 1 is broken in this case and never had a bug report so let's assume
    // it's not an issue. I don't think anyone ever specifies width on <html>
    // anyway.
    // Browsers where the left scrollbar doesn't cause an issue report `0` for
    // this (e.g. Edge 2019, IE11, Safari)
    return getBoundingClientRect(getDocumentElement(element)).left + getWindowScroll(element).scrollLeft;
  }

  function getViewportRect(element, strategy) {
    var win = getWindow(element);
    var html = getDocumentElement(element);
    var visualViewport = win.visualViewport;
    var width = html.clientWidth;
    var height = html.clientHeight;
    var x = 0;
    var y = 0;

    if (visualViewport) {
      width = visualViewport.width;
      height = visualViewport.height;
      var layoutViewport = isLayoutViewport();

      if (layoutViewport || !layoutViewport && strategy === 'fixed') {
        x = visualViewport.offsetLeft;
        y = visualViewport.offsetTop;
      }
    }

    return {
      width: width,
      height: height,
      x: x + getWindowScrollBarX(element),
      y: y
    };
  }

  // of the `<html>` and `<body>` rect bounds if horizontally scrollable

  function getDocumentRect(element) {
    var _element$ownerDocumen;

    var html = getDocumentElement(element);
    var winScroll = getWindowScroll(element);
    var body = (_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body;
    var width = max(html.scrollWidth, html.clientWidth, body ? body.scrollWidth : 0, body ? body.clientWidth : 0);
    var height = max(html.scrollHeight, html.clientHeight, body ? body.scrollHeight : 0, body ? body.clientHeight : 0);
    var x = -winScroll.scrollLeft + getWindowScrollBarX(element);
    var y = -winScroll.scrollTop;

    if (getComputedStyle$1(body || html).direction === 'rtl') {
      x += max(html.clientWidth, body ? body.clientWidth : 0) - width;
    }

    return {
      width: width,
      height: height,
      x: x,
      y: y
    };
  }

  function isScrollParent(element) {
    // Firefox wants us to check `-x` and `-y` variations as well
    var _getComputedStyle = getComputedStyle$1(element),
        overflow = _getComputedStyle.overflow,
        overflowX = _getComputedStyle.overflowX,
        overflowY = _getComputedStyle.overflowY;

    return /auto|scroll|overlay|hidden/.test(overflow + overflowY + overflowX);
  }

  function getScrollParent(node) {
    if (['html', 'body', '#document'].indexOf(getNodeName(node)) >= 0) {
      // $FlowFixMe[incompatible-return]: assume body is always available
      return node.ownerDocument.body;
    }

    if (isHTMLElement(node) && isScrollParent(node)) {
      return node;
    }

    return getScrollParent(getParentNode(node));
  }

  /*
  given a DOM element, return the list of all scroll parents, up the list of ancesors
  until we get to the top window object. This list is what we attach scroll listeners
  to, because if any of these parent elements scroll, we'll need to re-calculate the
  reference element's position.
  */

  function listScrollParents(element, list) {
    var _element$ownerDocumen;

    if (list === void 0) {
      list = [];
    }

    var scrollParent = getScrollParent(element);
    var isBody = scrollParent === ((_element$ownerDocumen = element.ownerDocument) == null ? void 0 : _element$ownerDocumen.body);
    var win = getWindow(scrollParent);
    var target = isBody ? [win].concat(win.visualViewport || [], isScrollParent(scrollParent) ? scrollParent : []) : scrollParent;
    var updatedList = list.concat(target);
    return isBody ? updatedList : // $FlowFixMe[incompatible-call]: isBody tells us target will be an HTMLElement here
    updatedList.concat(listScrollParents(getParentNode(target)));
  }

  function rectToClientRect(rect) {
    return Object.assign({}, rect, {
      left: rect.x,
      top: rect.y,
      right: rect.x + rect.width,
      bottom: rect.y + rect.height
    });
  }

  function getInnerBoundingClientRect(element, strategy) {
    var rect = getBoundingClientRect(element, false, strategy === 'fixed');
    rect.top = rect.top + element.clientTop;
    rect.left = rect.left + element.clientLeft;
    rect.bottom = rect.top + element.clientHeight;
    rect.right = rect.left + element.clientWidth;
    rect.width = element.clientWidth;
    rect.height = element.clientHeight;
    rect.x = rect.left;
    rect.y = rect.top;
    return rect;
  }

  function getClientRectFromMixedType(element, clippingParent, strategy) {
    return clippingParent === viewport ? rectToClientRect(getViewportRect(element, strategy)) : isElement(clippingParent) ? getInnerBoundingClientRect(clippingParent, strategy) : rectToClientRect(getDocumentRect(getDocumentElement(element)));
  } // A "clipping parent" is an overflowable container with the characteristic of
  // clipping (or hiding) overflowing elements with a position different from
  // `initial`


  function getClippingParents(element) {
    var clippingParents = listScrollParents(getParentNode(element));
    var canEscapeClipping = ['absolute', 'fixed'].indexOf(getComputedStyle$1(element).position) >= 0;
    var clipperElement = canEscapeClipping && isHTMLElement(element) ? getOffsetParent(element) : element;

    if (!isElement(clipperElement)) {
      return [];
    } // $FlowFixMe[incompatible-return]: https://github.com/facebook/flow/issues/1414


    return clippingParents.filter(function (clippingParent) {
      return isElement(clippingParent) && contains(clippingParent, clipperElement) && getNodeName(clippingParent) !== 'body';
    });
  } // Gets the maximum area that the element is visible in due to any number of
  // clipping parents


  function getClippingRect(element, boundary, rootBoundary, strategy) {
    var mainClippingParents = boundary === 'clippingParents' ? getClippingParents(element) : [].concat(boundary);
    var clippingParents = [].concat(mainClippingParents, [rootBoundary]);
    var firstClippingParent = clippingParents[0];
    var clippingRect = clippingParents.reduce(function (accRect, clippingParent) {
      var rect = getClientRectFromMixedType(element, clippingParent, strategy);
      accRect.top = max(rect.top, accRect.top);
      accRect.right = min(rect.right, accRect.right);
      accRect.bottom = min(rect.bottom, accRect.bottom);
      accRect.left = max(rect.left, accRect.left);
      return accRect;
    }, getClientRectFromMixedType(element, firstClippingParent, strategy));
    clippingRect.width = clippingRect.right - clippingRect.left;
    clippingRect.height = clippingRect.bottom - clippingRect.top;
    clippingRect.x = clippingRect.left;
    clippingRect.y = clippingRect.top;
    return clippingRect;
  }

  function computeOffsets(_ref) {
    var reference = _ref.reference,
        element = _ref.element,
        placement = _ref.placement;
    var basePlacement = placement ? getBasePlacement(placement) : null;
    var variation = placement ? getVariation(placement) : null;
    var commonX = reference.x + reference.width / 2 - element.width / 2;
    var commonY = reference.y + reference.height / 2 - element.height / 2;
    var offsets;

    switch (basePlacement) {
      case top:
        offsets = {
          x: commonX,
          y: reference.y - element.height
        };
        break;

      case bottom:
        offsets = {
          x: commonX,
          y: reference.y + reference.height
        };
        break;

      case right:
        offsets = {
          x: reference.x + reference.width,
          y: commonY
        };
        break;

      case left:
        offsets = {
          x: reference.x - element.width,
          y: commonY
        };
        break;

      default:
        offsets = {
          x: reference.x,
          y: reference.y
        };
    }

    var mainAxis = basePlacement ? getMainAxisFromPlacement(basePlacement) : null;

    if (mainAxis != null) {
      var len = mainAxis === 'y' ? 'height' : 'width';

      switch (variation) {
        case start:
          offsets[mainAxis] = offsets[mainAxis] - (reference[len] / 2 - element[len] / 2);
          break;

        case end:
          offsets[mainAxis] = offsets[mainAxis] + (reference[len] / 2 - element[len] / 2);
          break;
      }
    }

    return offsets;
  }

  function detectOverflow(state, options) {
    if (options === void 0) {
      options = {};
    }

    var _options = options,
        _options$placement = _options.placement,
        placement = _options$placement === void 0 ? state.placement : _options$placement,
        _options$strategy = _options.strategy,
        strategy = _options$strategy === void 0 ? state.strategy : _options$strategy,
        _options$boundary = _options.boundary,
        boundary = _options$boundary === void 0 ? clippingParents : _options$boundary,
        _options$rootBoundary = _options.rootBoundary,
        rootBoundary = _options$rootBoundary === void 0 ? viewport : _options$rootBoundary,
        _options$elementConte = _options.elementContext,
        elementContext = _options$elementConte === void 0 ? popper : _options$elementConte,
        _options$altBoundary = _options.altBoundary,
        altBoundary = _options$altBoundary === void 0 ? false : _options$altBoundary,
        _options$padding = _options.padding,
        padding = _options$padding === void 0 ? 0 : _options$padding;
    var paddingObject = mergePaddingObject(typeof padding !== 'number' ? padding : expandToHashMap(padding, basePlacements));
    var altContext = elementContext === popper ? reference : popper;
    var popperRect = state.rects.popper;
    var element = state.elements[altBoundary ? altContext : elementContext];
    var clippingClientRect = getClippingRect(isElement(element) ? element : element.contextElement || getDocumentElement(state.elements.popper), boundary, rootBoundary, strategy);
    var referenceClientRect = getBoundingClientRect(state.elements.reference);
    var popperOffsets = computeOffsets({
      reference: referenceClientRect,
      element: popperRect,
      strategy: 'absolute',
      placement: placement
    });
    var popperClientRect = rectToClientRect(Object.assign({}, popperRect, popperOffsets));
    var elementClientRect = elementContext === popper ? popperClientRect : referenceClientRect; // positive = overflowing the clipping rect
    // 0 or negative = within the clipping rect

    var overflowOffsets = {
      top: clippingClientRect.top - elementClientRect.top + paddingObject.top,
      bottom: elementClientRect.bottom - clippingClientRect.bottom + paddingObject.bottom,
      left: clippingClientRect.left - elementClientRect.left + paddingObject.left,
      right: elementClientRect.right - clippingClientRect.right + paddingObject.right
    };
    var offsetData = state.modifiersData.offset; // Offsets can be applied only to the popper element

    if (elementContext === popper && offsetData) {
      var offset = offsetData[placement];
      Object.keys(overflowOffsets).forEach(function (key) {
        var multiply = [right, bottom].indexOf(key) >= 0 ? 1 : -1;
        var axis = [top, bottom].indexOf(key) >= 0 ? 'y' : 'x';
        overflowOffsets[key] += offset[axis] * multiply;
      });
    }

    return overflowOffsets;
  }

  function computeAutoPlacement(state, options) {
    if (options === void 0) {
      options = {};
    }

    var _options = options,
        placement = _options.placement,
        boundary = _options.boundary,
        rootBoundary = _options.rootBoundary,
        padding = _options.padding,
        flipVariations = _options.flipVariations,
        _options$allowedAutoP = _options.allowedAutoPlacements,
        allowedAutoPlacements = _options$allowedAutoP === void 0 ? placements : _options$allowedAutoP;
    var variation = getVariation(placement);
    var placements$1 = variation ? flipVariations ? variationPlacements : variationPlacements.filter(function (placement) {
      return getVariation(placement) === variation;
    }) : basePlacements;
    var allowedPlacements = placements$1.filter(function (placement) {
      return allowedAutoPlacements.indexOf(placement) >= 0;
    });

    if (allowedPlacements.length === 0) {
      allowedPlacements = placements$1;
    } // $FlowFixMe[incompatible-type]: Flow seems to have problems with two array unions...


    var overflows = allowedPlacements.reduce(function (acc, placement) {
      acc[placement] = detectOverflow(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        padding: padding
      })[getBasePlacement(placement)];
      return acc;
    }, {});
    return Object.keys(overflows).sort(function (a, b) {
      return overflows[a] - overflows[b];
    });
  }

  function getExpandedFallbackPlacements(placement) {
    if (getBasePlacement(placement) === auto) {
      return [];
    }

    var oppositePlacement = getOppositePlacement(placement);
    return [getOppositeVariationPlacement(placement), oppositePlacement, getOppositeVariationPlacement(oppositePlacement)];
  }

  function flip(_ref) {
    var state = _ref.state,
        options = _ref.options,
        name = _ref.name;

    if (state.modifiersData[name]._skip) {
      return;
    }

    var _options$mainAxis = options.mainAxis,
        checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis,
        _options$altAxis = options.altAxis,
        checkAltAxis = _options$altAxis === void 0 ? true : _options$altAxis,
        specifiedFallbackPlacements = options.fallbackPlacements,
        padding = options.padding,
        boundary = options.boundary,
        rootBoundary = options.rootBoundary,
        altBoundary = options.altBoundary,
        _options$flipVariatio = options.flipVariations,
        flipVariations = _options$flipVariatio === void 0 ? true : _options$flipVariatio,
        allowedAutoPlacements = options.allowedAutoPlacements;
    var preferredPlacement = state.options.placement;
    var basePlacement = getBasePlacement(preferredPlacement);
    var isBasePlacement = basePlacement === preferredPlacement;
    var fallbackPlacements = specifiedFallbackPlacements || (isBasePlacement || !flipVariations ? [getOppositePlacement(preferredPlacement)] : getExpandedFallbackPlacements(preferredPlacement));
    var placements = [preferredPlacement].concat(fallbackPlacements).reduce(function (acc, placement) {
      return acc.concat(getBasePlacement(placement) === auto ? computeAutoPlacement(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        padding: padding,
        flipVariations: flipVariations,
        allowedAutoPlacements: allowedAutoPlacements
      }) : placement);
    }, []);
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var checksMap = new Map();
    var makeFallbackChecks = true;
    var firstFittingPlacement = placements[0];

    for (var i = 0; i < placements.length; i++) {
      var placement = placements[i];

      var _basePlacement = getBasePlacement(placement);

      var isStartVariation = getVariation(placement) === start;
      var isVertical = [top, bottom].indexOf(_basePlacement) >= 0;
      var len = isVertical ? 'width' : 'height';
      var overflow = detectOverflow(state, {
        placement: placement,
        boundary: boundary,
        rootBoundary: rootBoundary,
        altBoundary: altBoundary,
        padding: padding
      });
      var mainVariationSide = isVertical ? isStartVariation ? right : left : isStartVariation ? bottom : top;

      if (referenceRect[len] > popperRect[len]) {
        mainVariationSide = getOppositePlacement(mainVariationSide);
      }

      var altVariationSide = getOppositePlacement(mainVariationSide);
      var checks = [];

      if (checkMainAxis) {
        checks.push(overflow[_basePlacement] <= 0);
      }

      if (checkAltAxis) {
        checks.push(overflow[mainVariationSide] <= 0, overflow[altVariationSide] <= 0);
      }

      if (checks.every(function (check) {
        return check;
      })) {
        firstFittingPlacement = placement;
        makeFallbackChecks = false;
        break;
      }

      checksMap.set(placement, checks);
    }

    if (makeFallbackChecks) {
      // `2` may be desired in some cases – research later
      var numberOfChecks = flipVariations ? 3 : 1;

      var _loop = function _loop(_i) {
        var fittingPlacement = placements.find(function (placement) {
          var checks = checksMap.get(placement);

          if (checks) {
            return checks.slice(0, _i).every(function (check) {
              return check;
            });
          }
        });

        if (fittingPlacement) {
          firstFittingPlacement = fittingPlacement;
          return "break";
        }
      };

      for (var _i = numberOfChecks; _i > 0; _i--) {
        var _ret = _loop(_i);

        if (_ret === "break") break;
      }
    }

    if (state.placement !== firstFittingPlacement) {
      state.modifiersData[name]._skip = true;
      state.placement = firstFittingPlacement;
      state.reset = true;
    }
  } // eslint-disable-next-line import/no-unused-modules


  const flip$1 = {
    name: 'flip',
    enabled: true,
    phase: 'main',
    fn: flip,
    requiresIfExists: ['offset'],
    data: {
      _skip: false
    }
  };

  function getSideOffsets(overflow, rect, preventedOffsets) {
    if (preventedOffsets === void 0) {
      preventedOffsets = {
        x: 0,
        y: 0
      };
    }

    return {
      top: overflow.top - rect.height - preventedOffsets.y,
      right: overflow.right - rect.width + preventedOffsets.x,
      bottom: overflow.bottom - rect.height + preventedOffsets.y,
      left: overflow.left - rect.width - preventedOffsets.x
    };
  }

  function isAnySideFullyClipped(overflow) {
    return [top, right, bottom, left].some(function (side) {
      return overflow[side] >= 0;
    });
  }

  function hide(_ref) {
    var state = _ref.state,
        name = _ref.name;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var preventedOffsets = state.modifiersData.preventOverflow;
    var referenceOverflow = detectOverflow(state, {
      elementContext: 'reference'
    });
    var popperAltOverflow = detectOverflow(state, {
      altBoundary: true
    });
    var referenceClippingOffsets = getSideOffsets(referenceOverflow, referenceRect);
    var popperEscapeOffsets = getSideOffsets(popperAltOverflow, popperRect, preventedOffsets);
    var isReferenceHidden = isAnySideFullyClipped(referenceClippingOffsets);
    var hasPopperEscaped = isAnySideFullyClipped(popperEscapeOffsets);
    state.modifiersData[name] = {
      referenceClippingOffsets: referenceClippingOffsets,
      popperEscapeOffsets: popperEscapeOffsets,
      isReferenceHidden: isReferenceHidden,
      hasPopperEscaped: hasPopperEscaped
    };
    state.attributes.popper = Object.assign({}, state.attributes.popper, {
      'data-popper-reference-hidden': isReferenceHidden,
      'data-popper-escaped': hasPopperEscaped
    });
  } // eslint-disable-next-line import/no-unused-modules


  const hide$1 = {
    name: 'hide',
    enabled: true,
    phase: 'main',
    requiresIfExists: ['preventOverflow'],
    fn: hide
  };

  function distanceAndSkiddingToXY(placement, rects, offset) {
    var basePlacement = getBasePlacement(placement);
    var invertDistance = [left, top].indexOf(basePlacement) >= 0 ? -1 : 1;

    var _ref = typeof offset === 'function' ? offset(Object.assign({}, rects, {
      placement: placement
    })) : offset,
        skidding = _ref[0],
        distance = _ref[1];

    skidding = skidding || 0;
    distance = (distance || 0) * invertDistance;
    return [left, right].indexOf(basePlacement) >= 0 ? {
      x: distance,
      y: skidding
    } : {
      x: skidding,
      y: distance
    };
  }

  function offset(_ref2) {
    var state = _ref2.state,
        options = _ref2.options,
        name = _ref2.name;
    var _options$offset = options.offset,
        offset = _options$offset === void 0 ? [0, 0] : _options$offset;
    var data = placements.reduce(function (acc, placement) {
      acc[placement] = distanceAndSkiddingToXY(placement, state.rects, offset);
      return acc;
    }, {});
    var _data$state$placement = data[state.placement],
        x = _data$state$placement.x,
        y = _data$state$placement.y;

    if (state.modifiersData.popperOffsets != null) {
      state.modifiersData.popperOffsets.x += x;
      state.modifiersData.popperOffsets.y += y;
    }

    state.modifiersData[name] = data;
  } // eslint-disable-next-line import/no-unused-modules


  const offset$1 = {
    name: 'offset',
    enabled: true,
    phase: 'main',
    requires: ['popperOffsets'],
    fn: offset
  };

  function popperOffsets(_ref) {
    var state = _ref.state,
        name = _ref.name;
    // Offsets are the actual position the popper needs to have to be
    // properly positioned near its reference element
    // This is the most basic placement, and will be adjusted by
    // the modifiers in the next step
    state.modifiersData[name] = computeOffsets({
      reference: state.rects.reference,
      element: state.rects.popper,
      strategy: 'absolute',
      placement: state.placement
    });
  } // eslint-disable-next-line import/no-unused-modules


  const popperOffsets$1 = {
    name: 'popperOffsets',
    enabled: true,
    phase: 'read',
    fn: popperOffsets,
    data: {}
  };

  function getAltAxis(axis) {
    return axis === 'x' ? 'y' : 'x';
  }

  function preventOverflow(_ref) {
    var state = _ref.state,
        options = _ref.options,
        name = _ref.name;
    var _options$mainAxis = options.mainAxis,
        checkMainAxis = _options$mainAxis === void 0 ? true : _options$mainAxis,
        _options$altAxis = options.altAxis,
        checkAltAxis = _options$altAxis === void 0 ? false : _options$altAxis,
        boundary = options.boundary,
        rootBoundary = options.rootBoundary,
        altBoundary = options.altBoundary,
        padding = options.padding,
        _options$tether = options.tether,
        tether = _options$tether === void 0 ? true : _options$tether,
        _options$tetherOffset = options.tetherOffset,
        tetherOffset = _options$tetherOffset === void 0 ? 0 : _options$tetherOffset;
    var overflow = detectOverflow(state, {
      boundary: boundary,
      rootBoundary: rootBoundary,
      padding: padding,
      altBoundary: altBoundary
    });
    var basePlacement = getBasePlacement(state.placement);
    var variation = getVariation(state.placement);
    var isBasePlacement = !variation;
    var mainAxis = getMainAxisFromPlacement(basePlacement);
    var altAxis = getAltAxis(mainAxis);
    var popperOffsets = state.modifiersData.popperOffsets;
    var referenceRect = state.rects.reference;
    var popperRect = state.rects.popper;
    var tetherOffsetValue = typeof tetherOffset === 'function' ? tetherOffset(Object.assign({}, state.rects, {
      placement: state.placement
    })) : tetherOffset;
    var normalizedTetherOffsetValue = typeof tetherOffsetValue === 'number' ? {
      mainAxis: tetherOffsetValue,
      altAxis: tetherOffsetValue
    } : Object.assign({
      mainAxis: 0,
      altAxis: 0
    }, tetherOffsetValue);
    var offsetModifierState = state.modifiersData.offset ? state.modifiersData.offset[state.placement] : null;
    var data = {
      x: 0,
      y: 0
    };

    if (!popperOffsets) {
      return;
    }

    if (checkMainAxis) {
      var _offsetModifierState$;

      var mainSide = mainAxis === 'y' ? top : left;
      var altSide = mainAxis === 'y' ? bottom : right;
      var len = mainAxis === 'y' ? 'height' : 'width';
      var offset = popperOffsets[mainAxis];
      var min$1 = offset + overflow[mainSide];
      var max$1 = offset - overflow[altSide];
      var additive = tether ? -popperRect[len] / 2 : 0;
      var minLen = variation === start ? referenceRect[len] : popperRect[len];
      var maxLen = variation === start ? -popperRect[len] : -referenceRect[len]; // We need to include the arrow in the calculation so the arrow doesn't go
      // outside the reference bounds

      var arrowElement = state.elements.arrow;
      var arrowRect = tether && arrowElement ? getLayoutRect(arrowElement) : {
        width: 0,
        height: 0
      };
      var arrowPaddingObject = state.modifiersData['arrow#persistent'] ? state.modifiersData['arrow#persistent'].padding : getFreshSideObject();
      var arrowPaddingMin = arrowPaddingObject[mainSide];
      var arrowPaddingMax = arrowPaddingObject[altSide]; // If the reference length is smaller than the arrow length, we don't want
      // to include its full size in the calculation. If the reference is small
      // and near the edge of a boundary, the popper can overflow even if the
      // reference is not overflowing as well (e.g. virtual elements with no
      // width or height)

      var arrowLen = within(0, referenceRect[len], arrowRect[len]);
      var minOffset = isBasePlacement ? referenceRect[len] / 2 - additive - arrowLen - arrowPaddingMin - normalizedTetherOffsetValue.mainAxis : minLen - arrowLen - arrowPaddingMin - normalizedTetherOffsetValue.mainAxis;
      var maxOffset = isBasePlacement ? -referenceRect[len] / 2 + additive + arrowLen + arrowPaddingMax + normalizedTetherOffsetValue.mainAxis : maxLen + arrowLen + arrowPaddingMax + normalizedTetherOffsetValue.mainAxis;
      var arrowOffsetParent = state.elements.arrow && getOffsetParent(state.elements.arrow);
      var clientOffset = arrowOffsetParent ? mainAxis === 'y' ? arrowOffsetParent.clientTop || 0 : arrowOffsetParent.clientLeft || 0 : 0;
      var offsetModifierValue = (_offsetModifierState$ = offsetModifierState == null ? void 0 : offsetModifierState[mainAxis]) != null ? _offsetModifierState$ : 0;
      var tetherMin = offset + minOffset - offsetModifierValue - clientOffset;
      var tetherMax = offset + maxOffset - offsetModifierValue;
      var preventedOffset = within(tether ? min(min$1, tetherMin) : min$1, offset, tether ? max(max$1, tetherMax) : max$1);
      popperOffsets[mainAxis] = preventedOffset;
      data[mainAxis] = preventedOffset - offset;
    }

    if (checkAltAxis) {
      var _offsetModifierState$2;

      var _mainSide = mainAxis === 'x' ? top : left;

      var _altSide = mainAxis === 'x' ? bottom : right;

      var _offset = popperOffsets[altAxis];

      var _len = altAxis === 'y' ? 'height' : 'width';

      var _min = _offset + overflow[_mainSide];

      var _max = _offset - overflow[_altSide];

      var isOriginSide = [top, left].indexOf(basePlacement) !== -1;

      var _offsetModifierValue = (_offsetModifierState$2 = offsetModifierState == null ? void 0 : offsetModifierState[altAxis]) != null ? _offsetModifierState$2 : 0;

      var _tetherMin = isOriginSide ? _min : _offset - referenceRect[_len] - popperRect[_len] - _offsetModifierValue + normalizedTetherOffsetValue.altAxis;

      var _tetherMax = isOriginSide ? _offset + referenceRect[_len] + popperRect[_len] - _offsetModifierValue - normalizedTetherOffsetValue.altAxis : _max;

      var _preventedOffset = tether && isOriginSide ? withinMaxClamp(_tetherMin, _offset, _tetherMax) : within(tether ? _tetherMin : _min, _offset, tether ? _tetherMax : _max);

      popperOffsets[altAxis] = _preventedOffset;
      data[altAxis] = _preventedOffset - _offset;
    }

    state.modifiersData[name] = data;
  } // eslint-disable-next-line import/no-unused-modules


  const preventOverflow$1 = {
    name: 'preventOverflow',
    enabled: true,
    phase: 'main',
    fn: preventOverflow,
    requiresIfExists: ['offset']
  };

  function getHTMLElementScroll(element) {
    return {
      scrollLeft: element.scrollLeft,
      scrollTop: element.scrollTop
    };
  }

  function getNodeScroll(node) {
    if (node === getWindow(node) || !isHTMLElement(node)) {
      return getWindowScroll(node);
    } else {
      return getHTMLElementScroll(node);
    }
  }

  function isElementScaled(element) {
    var rect = element.getBoundingClientRect();
    var scaleX = round(rect.width) / element.offsetWidth || 1;
    var scaleY = round(rect.height) / element.offsetHeight || 1;
    return scaleX !== 1 || scaleY !== 1;
  } // Returns the composite rect of an element relative to its offsetParent.
  // Composite means it takes into account transforms as well as layout.


  function getCompositeRect(elementOrVirtualElement, offsetParent, isFixed) {
    if (isFixed === void 0) {
      isFixed = false;
    }

    var isOffsetParentAnElement = isHTMLElement(offsetParent);
    var offsetParentIsScaled = isHTMLElement(offsetParent) && isElementScaled(offsetParent);
    var documentElement = getDocumentElement(offsetParent);
    var rect = getBoundingClientRect(elementOrVirtualElement, offsetParentIsScaled, isFixed);
    var scroll = {
      scrollLeft: 0,
      scrollTop: 0
    };
    var offsets = {
      x: 0,
      y: 0
    };

    if (isOffsetParentAnElement || !isOffsetParentAnElement && !isFixed) {
      if (getNodeName(offsetParent) !== 'body' || // https://github.com/popperjs/popper-core/issues/1078
      isScrollParent(documentElement)) {
        scroll = getNodeScroll(offsetParent);
      }

      if (isHTMLElement(offsetParent)) {
        offsets = getBoundingClientRect(offsetParent, true);
        offsets.x += offsetParent.clientLeft;
        offsets.y += offsetParent.clientTop;
      } else if (documentElement) {
        offsets.x = getWindowScrollBarX(documentElement);
      }
    }

    return {
      x: rect.left + scroll.scrollLeft - offsets.x,
      y: rect.top + scroll.scrollTop - offsets.y,
      width: rect.width,
      height: rect.height
    };
  }

  function order(modifiers) {
    var map = new Map();
    var visited = new Set();
    var result = [];
    modifiers.forEach(function (modifier) {
      map.set(modifier.name, modifier);
    }); // On visiting object, check for its dependencies and visit them recursively

    function sort(modifier) {
      visited.add(modifier.name);
      var requires = [].concat(modifier.requires || [], modifier.requiresIfExists || []);
      requires.forEach(function (dep) {
        if (!visited.has(dep)) {
          var depModifier = map.get(dep);

          if (depModifier) {
            sort(depModifier);
          }
        }
      });
      result.push(modifier);
    }

    modifiers.forEach(function (modifier) {
      if (!visited.has(modifier.name)) {
        // check for visited object
        sort(modifier);
      }
    });
    return result;
  }

  function orderModifiers(modifiers) {
    // order based on dependencies
    var orderedModifiers = order(modifiers); // order based on phase

    return modifierPhases.reduce(function (acc, phase) {
      return acc.concat(orderedModifiers.filter(function (modifier) {
        return modifier.phase === phase;
      }));
    }, []);
  }

  function debounce(fn) {
    var pending;
    return function () {
      if (!pending) {
        pending = new Promise(function (resolve) {
          Promise.resolve().then(function () {
            pending = undefined;
            resolve(fn());
          });
        });
      }

      return pending;
    };
  }

  function mergeByName(modifiers) {
    var merged = modifiers.reduce(function (merged, current) {
      var existing = merged[current.name];
      merged[current.name] = existing ? Object.assign({}, existing, current, {
        options: Object.assign({}, existing.options, current.options),
        data: Object.assign({}, existing.data, current.data)
      }) : current;
      return merged;
    }, {}); // IE11 does not support Object.values

    return Object.keys(merged).map(function (key) {
      return merged[key];
    });
  }

  var DEFAULT_OPTIONS = {
    placement: 'bottom',
    modifiers: [],
    strategy: 'absolute'
  };

  function areValidElements() {
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }

    return !args.some(function (element) {
      return !(element && typeof element.getBoundingClientRect === 'function');
    });
  }

  function popperGenerator(generatorOptions) {
    if (generatorOptions === void 0) {
      generatorOptions = {};
    }

    var _generatorOptions = generatorOptions,
        _generatorOptions$def = _generatorOptions.defaultModifiers,
        defaultModifiers = _generatorOptions$def === void 0 ? [] : _generatorOptions$def,
        _generatorOptions$def2 = _generatorOptions.defaultOptions,
        defaultOptions = _generatorOptions$def2 === void 0 ? DEFAULT_OPTIONS : _generatorOptions$def2;
    return function createPopper(reference, popper, options) {
      if (options === void 0) {
        options = defaultOptions;
      }

      var state = {
        placement: 'bottom',
        orderedModifiers: [],
        options: Object.assign({}, DEFAULT_OPTIONS, defaultOptions),
        modifiersData: {},
        elements: {
          reference: reference,
          popper: popper
        },
        attributes: {},
        styles: {}
      };
      var effectCleanupFns = [];
      var isDestroyed = false;
      var instance = {
        state: state,
        setOptions: function setOptions(setOptionsAction) {
          var options = typeof setOptionsAction === 'function' ? setOptionsAction(state.options) : setOptionsAction;
          cleanupModifierEffects();
          state.options = Object.assign({}, defaultOptions, state.options, options);
          state.scrollParents = {
            reference: isElement(reference) ? listScrollParents(reference) : reference.contextElement ? listScrollParents(reference.contextElement) : [],
            popper: listScrollParents(popper)
          }; // Orders the modifiers based on their dependencies and `phase`
          // properties

          var orderedModifiers = orderModifiers(mergeByName([].concat(defaultModifiers, state.options.modifiers))); // Strip out disabled modifiers

          state.orderedModifiers = orderedModifiers.filter(function (m) {
            return m.enabled;
          });
          runModifierEffects();
          return instance.update();
        },
        // Sync update – it will always be executed, even if not necessary. This
        // is useful for low frequency updates where sync behavior simplifies the
        // logic.
        // For high frequency updates (e.g. `resize` and `scroll` events), always
        // prefer the async Popper#update method
        forceUpdate: function forceUpdate() {
          if (isDestroyed) {
            return;
          }

          var _state$elements = state.elements,
              reference = _state$elements.reference,
              popper = _state$elements.popper; // Don't proceed if `reference` or `popper` are not valid elements
          // anymore

          if (!areValidElements(reference, popper)) {
            return;
          } // Store the reference and popper rects to be read by modifiers


          state.rects = {
            reference: getCompositeRect(reference, getOffsetParent(popper), state.options.strategy === 'fixed'),
            popper: getLayoutRect(popper)
          }; // Modifiers have the ability to reset the current update cycle. The
          // most common use case for this is the `flip` modifier changing the
          // placement, which then needs to re-run all the modifiers, because the
          // logic was previously ran for the previous placement and is therefore
          // stale/incorrect

          state.reset = false;
          state.placement = state.options.placement; // On each update cycle, the `modifiersData` property for each modifier
          // is filled with the initial data specified by the modifier. This means
          // it doesn't persist and is fresh on each update.
          // To ensure persistent data, use `${name}#persistent`

          state.orderedModifiers.forEach(function (modifier) {
            return state.modifiersData[modifier.name] = Object.assign({}, modifier.data);
          });

          for (var index = 0; index < state.orderedModifiers.length; index++) {
            if (state.reset === true) {
              state.reset = false;
              index = -1;
              continue;
            }

            var _state$orderedModifie = state.orderedModifiers[index],
                fn = _state$orderedModifie.fn,
                _state$orderedModifie2 = _state$orderedModifie.options,
                _options = _state$orderedModifie2 === void 0 ? {} : _state$orderedModifie2,
                name = _state$orderedModifie.name;

            if (typeof fn === 'function') {
              state = fn({
                state: state,
                options: _options,
                name: name,
                instance: instance
              }) || state;
            }
          }
        },
        // Async and optimistically optimized update – it will not be executed if
        // not necessary (debounced to run at most once-per-tick)
        update: debounce(function () {
          return new Promise(function (resolve) {
            instance.forceUpdate();
            resolve(state);
          });
        }),
        destroy: function destroy() {
          cleanupModifierEffects();
          isDestroyed = true;
        }
      };

      if (!areValidElements(reference, popper)) {
        return instance;
      }

      instance.setOptions(options).then(function (state) {
        if (!isDestroyed && options.onFirstUpdate) {
          options.onFirstUpdate(state);
        }
      }); // Modifiers have the ability to execute arbitrary code before the first
      // update cycle runs. They will be executed in the same order as the update
      // cycle. This is useful when a modifier adds some persistent data that
      // other modifiers need to use, but the modifier is run after the dependent
      // one.

      function runModifierEffects() {
        state.orderedModifiers.forEach(function (_ref) {
          var name = _ref.name,
              _ref$options = _ref.options,
              options = _ref$options === void 0 ? {} : _ref$options,
              effect = _ref.effect;

          if (typeof effect === 'function') {
            var cleanupFn = effect({
              state: state,
              name: name,
              instance: instance,
              options: options
            });

            var noopFn = function noopFn() {};

            effectCleanupFns.push(cleanupFn || noopFn);
          }
        });
      }

      function cleanupModifierEffects() {
        effectCleanupFns.forEach(function (fn) {
          return fn();
        });
        effectCleanupFns = [];
      }

      return instance;
    };
  }
  var createPopper$2 = /*#__PURE__*/popperGenerator(); // eslint-disable-next-line import/no-unused-modules

  var defaultModifiers$1 = [eventListeners, popperOffsets$1, computeStyles$1, applyStyles$1];
  var createPopper$1 = /*#__PURE__*/popperGenerator({
    defaultModifiers: defaultModifiers$1
  }); // eslint-disable-next-line import/no-unused-modules

  var defaultModifiers = [eventListeners, popperOffsets$1, computeStyles$1, applyStyles$1, offset$1, flip$1, preventOverflow$1, arrow$1, hide$1];
  var createPopper = /*#__PURE__*/popperGenerator({
    defaultModifiers: defaultModifiers
  }); // eslint-disable-next-line import/no-unused-modules

  const Popper = /*#__PURE__*/Object.freeze(/*#__PURE__*/Object.defineProperty({
    __proto__: null,
    afterMain,
    afterRead,
    afterWrite,
    applyStyles: applyStyles$1,
    arrow: arrow$1,
    auto,
    basePlacements,
    beforeMain,
    beforeRead,
    beforeWrite,
    bottom,
    clippingParents,
    computeStyles: computeStyles$1,
    createPopper,
    createPopperBase: createPopper$2,
    createPopperLite: createPopper$1,
    detectOverflow,
    end,
    eventListeners,
    flip: flip$1,
    hide: hide$1,
    left,
    main,
    modifierPhases,
    offset: offset$1,
    placements,
    popper,
    popperGenerator,
    popperOffsets: popperOffsets$1,
    preventOverflow: preventOverflow$1,
    read,
    reference,
    right,
    start,
    top,
    variationPlacements,
    viewport,
    write
  }, Symbol.toStringTag, { value: 'Module' }));

  /**
   * --------------------------------------------------------------------------
   * Bootstrap dropdown.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$a = 'dropdown';
  const DATA_KEY$6 = 'bs.dropdown';
  const EVENT_KEY$6 = `.${DATA_KEY$6}`;
  const DATA_API_KEY$3 = '.data-api';
  const ESCAPE_KEY$2 = 'Escape';
  const TAB_KEY$1 = 'Tab';
  const ARROW_UP_KEY$1 = 'ArrowUp';
  const ARROW_DOWN_KEY$1 = 'ArrowDown';
  const RIGHT_MOUSE_BUTTON = 2; // MouseEvent.button value for the secondary button, usually the right button

  const EVENT_HIDE$5 = `hide${EVENT_KEY$6}`;
  const EVENT_HIDDEN$5 = `hidden${EVENT_KEY$6}`;
  const EVENT_SHOW$5 = `show${EVENT_KEY$6}`;
  const EVENT_SHOWN$5 = `shown${EVENT_KEY$6}`;
  const EVENT_CLICK_DATA_API$3 = `click${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const EVENT_KEYDOWN_DATA_API = `keydown${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const EVENT_KEYUP_DATA_API = `keyup${EVENT_KEY$6}${DATA_API_KEY$3}`;
  const CLASS_NAME_SHOW$6 = 'show';
  const CLASS_NAME_DROPUP = 'dropup';
  const CLASS_NAME_DROPEND = 'dropend';
  const CLASS_NAME_DROPSTART = 'dropstart';
  const CLASS_NAME_DROPUP_CENTER = 'dropup-center';
  const CLASS_NAME_DROPDOWN_CENTER = 'dropdown-center';
  const SELECTOR_DATA_TOGGLE$3 = '[data-bs-toggle="dropdown"]:not(.disabled):not(:disabled)';
  const SELECTOR_DATA_TOGGLE_SHOWN = `${SELECTOR_DATA_TOGGLE$3}.${CLASS_NAME_SHOW$6}`;
  const SELECTOR_MENU = '.dropdown-menu';
  const SELECTOR_NAVBAR = '.navbar';
  const SELECTOR_NAVBAR_NAV = '.navbar-nav';
  const SELECTOR_VISIBLE_ITEMS = '.dropdown-menu .dropdown-item:not(.disabled):not(:disabled)';
  const PLACEMENT_TOP = isRTL() ? 'top-end' : 'top-start';
  const PLACEMENT_TOPEND = isRTL() ? 'top-start' : 'top-end';
  const PLACEMENT_BOTTOM = isRTL() ? 'bottom-end' : 'bottom-start';
  const PLACEMENT_BOTTOMEND = isRTL() ? 'bottom-start' : 'bottom-end';
  const PLACEMENT_RIGHT = isRTL() ? 'left-start' : 'right-start';
  const PLACEMENT_LEFT = isRTL() ? 'right-start' : 'left-start';
  const PLACEMENT_TOPCENTER = 'top';
  const PLACEMENT_BOTTOMCENTER = 'bottom';
  const Default$9 = {
    autoClose: true,
    boundary: 'clippingParents',
    display: 'dynamic',
    offset: [0, 2],
    popperConfig: null,
    reference: 'toggle'
  };
  const DefaultType$9 = {
    autoClose: '(boolean|string)',
    boundary: '(string|element)',
    display: 'string',
    offset: '(array|string|function)',
    popperConfig: '(null|object|function)',
    reference: '(string|element|object)'
  };

  /**
   * Class definition
   */

  class Dropdown extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._popper = null;
      this._parent = this._element.parentNode; // dropdown wrapper
      // TODO: v6 revert #37011 & change markup https://getbootstrap.com/docs/5.3/forms/input-group/
      this._menu = SelectorEngine.next(this._element, SELECTOR_MENU)[0] || SelectorEngine.prev(this._element, SELECTOR_MENU)[0] || SelectorEngine.findOne(SELECTOR_MENU, this._parent);
      this._inNavbar = this._detectNavbar();
    }

    // Getters
    static get Default() {
      return Default$9;
    }
    static get DefaultType() {
      return DefaultType$9;
    }
    static get NAME() {
      return NAME$a;
    }

    // Public
    toggle() {
      return this._isShown() ? this.hide() : this.show();
    }
    show() {
      if (isDisabled(this._element) || this._isShown()) {
        return;
      }
      const relatedTarget = {
        relatedTarget: this._element
      };
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$5, relatedTarget);
      if (showEvent.defaultPrevented) {
        return;
      }
      this._createPopper();

      // If this is a touch-enabled device we add extra
      // empty mouseover listeners to the body's immediate children;
      // only needed because of broken event delegation on iOS
      // https://www.quirksmode.org/blog/archives/2014/02/mouse_event_bub.html
      if ('ontouchstart' in document.documentElement && !this._parent.closest(SELECTOR_NAVBAR_NAV)) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.on(element, 'mouseover', noop);
        }
      }
      this._element.focus();
      this._element.setAttribute('aria-expanded', true);
      this._menu.classList.add(CLASS_NAME_SHOW$6);
      this._element.classList.add(CLASS_NAME_SHOW$6);
      EventHandler.trigger(this._element, EVENT_SHOWN$5, relatedTarget);
    }
    hide() {
      if (isDisabled(this._element) || !this._isShown()) {
        return;
      }
      const relatedTarget = {
        relatedTarget: this._element
      };
      this._completeHide(relatedTarget);
    }
    dispose() {
      if (this._popper) {
        this._popper.destroy();
      }
      super.dispose();
    }
    update() {
      this._inNavbar = this._detectNavbar();
      if (this._popper) {
        this._popper.update();
      }
    }

    // Private
    _completeHide(relatedTarget) {
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$5, relatedTarget);
      if (hideEvent.defaultPrevented) {
        return;
      }

      // If this is a touch-enabled device we remove the extra
      // empty mouseover listeners we added for iOS support
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.off(element, 'mouseover', noop);
        }
      }
      if (this._popper) {
        this._popper.destroy();
      }
      this._menu.classList.remove(CLASS_NAME_SHOW$6);
      this._element.classList.remove(CLASS_NAME_SHOW$6);
      this._element.setAttribute('aria-expanded', 'false');
      Manipulator.removeDataAttribute(this._menu, 'popper');
      EventHandler.trigger(this._element, EVENT_HIDDEN$5, relatedTarget);
    }
    _getConfig(config) {
      config = super._getConfig(config);
      if (typeof config.reference === 'object' && !isElement$1(config.reference) && typeof config.reference.getBoundingClientRect !== 'function') {
        // Popper virtual elements require a getBoundingClientRect method
        throw new TypeError(`${NAME$a.toUpperCase()}: Option "reference" provided type "object" without a required "getBoundingClientRect" method.`);
      }
      return config;
    }
    _createPopper() {
      if (typeof Popper === 'undefined') {
        throw new TypeError('Bootstrap\'s dropdowns require Popper (https://popper.js.org)');
      }
      let referenceElement = this._element;
      if (this._config.reference === 'parent') {
        referenceElement = this._parent;
      } else if (isElement$1(this._config.reference)) {
        referenceElement = getElement(this._config.reference);
      } else if (typeof this._config.reference === 'object') {
        referenceElement = this._config.reference;
      }
      const popperConfig = this._getPopperConfig();
      this._popper = createPopper(referenceElement, this._menu, popperConfig);
    }
    _isShown() {
      return this._menu.classList.contains(CLASS_NAME_SHOW$6);
    }
    _getPlacement() {
      const parentDropdown = this._parent;
      if (parentDropdown.classList.contains(CLASS_NAME_DROPEND)) {
        return PLACEMENT_RIGHT;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPSTART)) {
        return PLACEMENT_LEFT;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPUP_CENTER)) {
        return PLACEMENT_TOPCENTER;
      }
      if (parentDropdown.classList.contains(CLASS_NAME_DROPDOWN_CENTER)) {
        return PLACEMENT_BOTTOMCENTER;
      }

      // We need to trim the value because custom properties can also include spaces
      const isEnd = getComputedStyle(this._menu).getPropertyValue('--bs-position').trim() === 'end';
      if (parentDropdown.classList.contains(CLASS_NAME_DROPUP)) {
        return isEnd ? PLACEMENT_TOPEND : PLACEMENT_TOP;
      }
      return isEnd ? PLACEMENT_BOTTOMEND : PLACEMENT_BOTTOM;
    }
    _detectNavbar() {
      return this._element.closest(SELECTOR_NAVBAR) !== null;
    }
    _getOffset() {
      const {
        offset
      } = this._config;
      if (typeof offset === 'string') {
        return offset.split(',').map(value => Number.parseInt(value, 10));
      }
      if (typeof offset === 'function') {
        return popperData => offset(popperData, this._element);
      }
      return offset;
    }
    _getPopperConfig() {
      const defaultBsPopperConfig = {
        placement: this._getPlacement(),
        modifiers: [{
          name: 'preventOverflow',
          options: {
            boundary: this._config.boundary
          }
        }, {
          name: 'offset',
          options: {
            offset: this._getOffset()
          }
        }]
      };

      // Disable Popper if we have a static display or Dropdown is in Navbar
      if (this._inNavbar || this._config.display === 'static') {
        Manipulator.setDataAttribute(this._menu, 'popper', 'static'); // TODO: v6 remove
        defaultBsPopperConfig.modifiers = [{
          name: 'applyStyles',
          enabled: false
        }];
      }
      return {
        ...defaultBsPopperConfig,
        ...execute(this._config.popperConfig, [defaultBsPopperConfig])
      };
    }
    _selectMenuItem({
      key,
      target
    }) {
      const items = SelectorEngine.find(SELECTOR_VISIBLE_ITEMS, this._menu).filter(element => isVisible(element));
      if (!items.length) {
        return;
      }

      // if target isn't included in items (e.g. when expanding the dropdown)
      // allow cycling to get the last item in case key equals ARROW_UP_KEY
      getNextActiveElement(items, target, key === ARROW_DOWN_KEY$1, !items.includes(target)).focus();
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Dropdown.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
    static clearMenus(event) {
      if (event.button === RIGHT_MOUSE_BUTTON || event.type === 'keyup' && event.key !== TAB_KEY$1) {
        return;
      }
      const openToggles = SelectorEngine.find(SELECTOR_DATA_TOGGLE_SHOWN);
      for (const toggle of openToggles) {
        const context = Dropdown.getInstance(toggle);
        if (!context || context._config.autoClose === false) {
          continue;
        }
        const composedPath = event.composedPath();
        const isMenuTarget = composedPath.includes(context._menu);
        if (composedPath.includes(context._element) || context._config.autoClose === 'inside' && !isMenuTarget || context._config.autoClose === 'outside' && isMenuTarget) {
          continue;
        }

        // Tab navigation through the dropdown menu or events from contained inputs shouldn't close the menu
        if (context._menu.contains(event.target) && (event.type === 'keyup' && event.key === TAB_KEY$1 || /input|select|option|textarea|form/i.test(event.target.tagName))) {
          continue;
        }
        const relatedTarget = {
          relatedTarget: context._element
        };
        if (event.type === 'click') {
          relatedTarget.clickEvent = event;
        }
        context._completeHide(relatedTarget);
      }
    }
    static dataApiKeydownHandler(event) {
      // If not an UP | DOWN | ESCAPE key => not a dropdown command
      // If input/textarea && if key is other than ESCAPE => not a dropdown command

      const isInput = /input|textarea/i.test(event.target.tagName);
      const isEscapeEvent = event.key === ESCAPE_KEY$2;
      const isUpOrDownEvent = [ARROW_UP_KEY$1, ARROW_DOWN_KEY$1].includes(event.key);
      if (!isUpOrDownEvent && !isEscapeEvent) {
        return;
      }
      if (isInput && !isEscapeEvent) {
        return;
      }
      event.preventDefault();

      // TODO: v6 revert #37011 & change markup https://getbootstrap.com/docs/5.3/forms/input-group/
      const getToggleButton = this.matches(SELECTOR_DATA_TOGGLE$3) ? this : SelectorEngine.prev(this, SELECTOR_DATA_TOGGLE$3)[0] || SelectorEngine.next(this, SELECTOR_DATA_TOGGLE$3)[0] || SelectorEngine.findOne(SELECTOR_DATA_TOGGLE$3, event.delegateTarget.parentNode);
      const instance = Dropdown.getOrCreateInstance(getToggleButton);
      if (isUpOrDownEvent) {
        event.stopPropagation();
        instance.show();
        instance._selectMenuItem(event);
        return;
      }
      if (instance._isShown()) {
        // else is escape and we check if it is shown
        event.stopPropagation();
        instance.hide();
        getToggleButton.focus();
      }
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_KEYDOWN_DATA_API, SELECTOR_DATA_TOGGLE$3, Dropdown.dataApiKeydownHandler);
  EventHandler.on(document, EVENT_KEYDOWN_DATA_API, SELECTOR_MENU, Dropdown.dataApiKeydownHandler);
  EventHandler.on(document, EVENT_CLICK_DATA_API$3, Dropdown.clearMenus);
  EventHandler.on(document, EVENT_KEYUP_DATA_API, Dropdown.clearMenus);
  EventHandler.on(document, EVENT_CLICK_DATA_API$3, SELECTOR_DATA_TOGGLE$3, function (event) {
    event.preventDefault();
    Dropdown.getOrCreateInstance(this).toggle();
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(Dropdown);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/backdrop.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$9 = 'backdrop';
  const CLASS_NAME_FADE$4 = 'fade';
  const CLASS_NAME_SHOW$5 = 'show';
  const EVENT_MOUSEDOWN = `mousedown.bs.${NAME$9}`;
  const Default$8 = {
    className: 'modal-backdrop',
    clickCallback: null,
    isAnimated: false,
    isVisible: true,
    // if false, we use the backdrop helper without adding any element to the dom
    rootElement: 'body' // give the choice to place backdrop under different elements
  };
  const DefaultType$8 = {
    className: 'string',
    clickCallback: '(function|null)',
    isAnimated: 'boolean',
    isVisible: 'boolean',
    rootElement: '(element|string)'
  };

  /**
   * Class definition
   */

  class Backdrop extends Config {
    constructor(config) {
      super();
      this._config = this._getConfig(config);
      this._isAppended = false;
      this._element = null;
    }

    // Getters
    static get Default() {
      return Default$8;
    }
    static get DefaultType() {
      return DefaultType$8;
    }
    static get NAME() {
      return NAME$9;
    }

    // Public
    show(callback) {
      if (!this._config.isVisible) {
        execute(callback);
        return;
      }
      this._append();
      const element = this._getElement();
      if (this._config.isAnimated) {
        reflow(element);
      }
      element.classList.add(CLASS_NAME_SHOW$5);
      this._emulateAnimation(() => {
        execute(callback);
      });
    }
    hide(callback) {
      if (!this._config.isVisible) {
        execute(callback);
        return;
      }
      this._getElement().classList.remove(CLASS_NAME_SHOW$5);
      this._emulateAnimation(() => {
        this.dispose();
        execute(callback);
      });
    }
    dispose() {
      if (!this._isAppended) {
        return;
      }
      EventHandler.off(this._element, EVENT_MOUSEDOWN);
      this._element.remove();
      this._isAppended = false;
    }

    // Private
    _getElement() {
      if (!this._element) {
        const backdrop = document.createElement('div');
        backdrop.className = this._config.className;
        if (this._config.isAnimated) {
          backdrop.classList.add(CLASS_NAME_FADE$4);
        }
        this._element = backdrop;
      }
      return this._element;
    }
    _configAfterMerge(config) {
      // use getElement() with the default "body" to get a fresh Element on each instantiation
      config.rootElement = getElement(config.rootElement);
      return config;
    }
    _append() {
      if (this._isAppended) {
        return;
      }
      const element = this._getElement();
      this._config.rootElement.append(element);
      EventHandler.on(element, EVENT_MOUSEDOWN, () => {
        execute(this._config.clickCallback);
      });
      this._isAppended = true;
    }
    _emulateAnimation(callback) {
      executeAfterTransition(callback, this._getElement(), this._config.isAnimated);
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/focustrap.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$8 = 'focustrap';
  const DATA_KEY$5 = 'bs.focustrap';
  const EVENT_KEY$5 = `.${DATA_KEY$5}`;
  const EVENT_FOCUSIN$2 = `focusin${EVENT_KEY$5}`;
  const EVENT_KEYDOWN_TAB = `keydown.tab${EVENT_KEY$5}`;
  const TAB_KEY = 'Tab';
  const TAB_NAV_FORWARD = 'forward';
  const TAB_NAV_BACKWARD = 'backward';
  const Default$7 = {
    autofocus: true,
    trapElement: null // The element to trap focus inside of
  };
  const DefaultType$7 = {
    autofocus: 'boolean',
    trapElement: 'element'
  };

  /**
   * Class definition
   */

  class FocusTrap extends Config {
    constructor(config) {
      super();
      this._config = this._getConfig(config);
      this._isActive = false;
      this._lastTabNavDirection = null;
    }

    // Getters
    static get Default() {
      return Default$7;
    }
    static get DefaultType() {
      return DefaultType$7;
    }
    static get NAME() {
      return NAME$8;
    }

    // Public
    activate() {
      if (this._isActive) {
        return;
      }
      if (this._config.autofocus) {
        this._config.trapElement.focus();
      }
      EventHandler.off(document, EVENT_KEY$5); // guard against infinite focus loop
      EventHandler.on(document, EVENT_FOCUSIN$2, event => this._handleFocusin(event));
      EventHandler.on(document, EVENT_KEYDOWN_TAB, event => this._handleKeydown(event));
      this._isActive = true;
    }
    deactivate() {
      if (!this._isActive) {
        return;
      }
      this._isActive = false;
      EventHandler.off(document, EVENT_KEY$5);
    }

    // Private
    _handleFocusin(event) {
      const {
        trapElement
      } = this._config;
      if (event.target === document || event.target === trapElement || trapElement.contains(event.target)) {
        return;
      }
      const elements = SelectorEngine.focusableChildren(trapElement);
      if (elements.length === 0) {
        trapElement.focus();
      } else if (this._lastTabNavDirection === TAB_NAV_BACKWARD) {
        elements[elements.length - 1].focus();
      } else {
        elements[0].focus();
      }
    }
    _handleKeydown(event) {
      if (event.key !== TAB_KEY) {
        return;
      }
      this._lastTabNavDirection = event.shiftKey ? TAB_NAV_BACKWARD : TAB_NAV_FORWARD;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/scrollBar.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const SELECTOR_FIXED_CONTENT = '.fixed-top, .fixed-bottom, .is-fixed, .sticky-top';
  const SELECTOR_STICKY_CONTENT = '.sticky-top';
  const PROPERTY_PADDING = 'padding-right';
  const PROPERTY_MARGIN = 'margin-right';

  /**
   * Class definition
   */

  class ScrollBarHelper {
    constructor() {
      this._element = document.body;
    }

    // Public
    getWidth() {
      // https://developer.mozilla.org/en-US/docs/Web/API/Window/innerWidth#usage_notes
      const documentWidth = document.documentElement.clientWidth;
      return Math.abs(window.innerWidth - documentWidth);
    }
    hide() {
      const width = this.getWidth();
      this._disableOverFlow();
      // give padding to element to balance the hidden scrollbar width
      this._setElementAttributes(this._element, PROPERTY_PADDING, calculatedValue => calculatedValue + width);
      // trick: We adjust positive paddingRight and negative marginRight to sticky-top elements to keep showing fullwidth
      this._setElementAttributes(SELECTOR_FIXED_CONTENT, PROPERTY_PADDING, calculatedValue => calculatedValue + width);
      this._setElementAttributes(SELECTOR_STICKY_CONTENT, PROPERTY_MARGIN, calculatedValue => calculatedValue - width);
    }
    reset() {
      this._resetElementAttributes(this._element, 'overflow');
      this._resetElementAttributes(this._element, PROPERTY_PADDING);
      this._resetElementAttributes(SELECTOR_FIXED_CONTENT, PROPERTY_PADDING);
      this._resetElementAttributes(SELECTOR_STICKY_CONTENT, PROPERTY_MARGIN);
    }
    isOverflowing() {
      return this.getWidth() > 0;
    }

    // Private
    _disableOverFlow() {
      this._saveInitialAttribute(this._element, 'overflow');
      this._element.style.overflow = 'hidden';
    }
    _setElementAttributes(selector, styleProperty, callback) {
      const scrollbarWidth = this.getWidth();
      const manipulationCallBack = element => {
        if (element !== this._element && window.innerWidth > element.clientWidth + scrollbarWidth) {
          return;
        }
        this._saveInitialAttribute(element, styleProperty);
        const calculatedValue = window.getComputedStyle(element).getPropertyValue(styleProperty);
        element.style.setProperty(styleProperty, `${callback(Number.parseFloat(calculatedValue))}px`);
      };
      this._applyManipulationCallback(selector, manipulationCallBack);
    }
    _saveInitialAttribute(element, styleProperty) {
      const actualValue = element.style.getPropertyValue(styleProperty);
      if (actualValue) {
        Manipulator.setDataAttribute(element, styleProperty, actualValue);
      }
    }
    _resetElementAttributes(selector, styleProperty) {
      const manipulationCallBack = element => {
        const value = Manipulator.getDataAttribute(element, styleProperty);
        // We only want to remove the property if the value is `null`; the value can also be zero
        if (value === null) {
          element.style.removeProperty(styleProperty);
          return;
        }
        Manipulator.removeDataAttribute(element, styleProperty);
        element.style.setProperty(styleProperty, value);
      };
      this._applyManipulationCallback(selector, manipulationCallBack);
    }
    _applyManipulationCallback(selector, callBack) {
      if (isElement$1(selector)) {
        callBack(selector);
        return;
      }
      for (const sel of SelectorEngine.find(selector, this._element)) {
        callBack(sel);
      }
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap modal.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$7 = 'modal';
  const DATA_KEY$4 = 'bs.modal';
  const EVENT_KEY$4 = `.${DATA_KEY$4}`;
  const DATA_API_KEY$2 = '.data-api';
  const ESCAPE_KEY$1 = 'Escape';
  const EVENT_HIDE$4 = `hide${EVENT_KEY$4}`;
  const EVENT_HIDE_PREVENTED$1 = `hidePrevented${EVENT_KEY$4}`;
  const EVENT_HIDDEN$4 = `hidden${EVENT_KEY$4}`;
  const EVENT_SHOW$4 = `show${EVENT_KEY$4}`;
  const EVENT_SHOWN$4 = `shown${EVENT_KEY$4}`;
  const EVENT_RESIZE$1 = `resize${EVENT_KEY$4}`;
  const EVENT_CLICK_DISMISS = `click.dismiss${EVENT_KEY$4}`;
  const EVENT_MOUSEDOWN_DISMISS = `mousedown.dismiss${EVENT_KEY$4}`;
  const EVENT_KEYDOWN_DISMISS$1 = `keydown.dismiss${EVENT_KEY$4}`;
  const EVENT_CLICK_DATA_API$2 = `click${EVENT_KEY$4}${DATA_API_KEY$2}`;
  const CLASS_NAME_OPEN = 'modal-open';
  const CLASS_NAME_FADE$3 = 'fade';
  const CLASS_NAME_SHOW$4 = 'show';
  const CLASS_NAME_STATIC = 'modal-static';
  const OPEN_SELECTOR$1 = '.modal.show';
  const SELECTOR_DIALOG = '.modal-dialog';
  const SELECTOR_MODAL_BODY = '.modal-body';
  const SELECTOR_DATA_TOGGLE$2 = '[data-bs-toggle="modal"]';
  const Default$6 = {
    backdrop: true,
    focus: true,
    keyboard: true
  };
  const DefaultType$6 = {
    backdrop: '(boolean|string)',
    focus: 'boolean',
    keyboard: 'boolean'
  };

  /**
   * Class definition
   */

  class Modal extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._dialog = SelectorEngine.findOne(SELECTOR_DIALOG, this._element);
      this._backdrop = this._initializeBackDrop();
      this._focustrap = this._initializeFocusTrap();
      this._isShown = false;
      this._isTransitioning = false;
      this._scrollBar = new ScrollBarHelper();
      this._addEventListeners();
    }

    // Getters
    static get Default() {
      return Default$6;
    }
    static get DefaultType() {
      return DefaultType$6;
    }
    static get NAME() {
      return NAME$7;
    }

    // Public
    toggle(relatedTarget) {
      return this._isShown ? this.hide() : this.show(relatedTarget);
    }
    show(relatedTarget) {
      if (this._isShown || this._isTransitioning) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$4, {
        relatedTarget
      });
      if (showEvent.defaultPrevented) {
        return;
      }
      this._isShown = true;
      this._isTransitioning = true;
      this._scrollBar.hide();
      document.body.classList.add(CLASS_NAME_OPEN);
      this._adjustDialog();
      this._backdrop.show(() => this._showElement(relatedTarget));
    }
    hide() {
      if (!this._isShown || this._isTransitioning) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$4);
      if (hideEvent.defaultPrevented) {
        return;
      }
      this._isShown = false;
      this._isTransitioning = true;
      this._focustrap.deactivate();
      this._element.classList.remove(CLASS_NAME_SHOW$4);
      this._queueCallback(() => this._hideModal(), this._element, this._isAnimated());
    }
    dispose() {
      EventHandler.off(window, EVENT_KEY$4);
      EventHandler.off(this._dialog, EVENT_KEY$4);
      this._backdrop.dispose();
      this._focustrap.deactivate();
      super.dispose();
    }
    handleUpdate() {
      this._adjustDialog();
    }

    // Private
    _initializeBackDrop() {
      return new Backdrop({
        isVisible: Boolean(this._config.backdrop),
        // 'static' option will be translated to true, and booleans will keep their value,
        isAnimated: this._isAnimated()
      });
    }
    _initializeFocusTrap() {
      return new FocusTrap({
        trapElement: this._element
      });
    }
    _showElement(relatedTarget) {
      // try to append dynamic modal
      if (!document.body.contains(this._element)) {
        document.body.append(this._element);
      }
      this._element.style.display = 'block';
      this._element.removeAttribute('aria-hidden');
      this._element.setAttribute('aria-modal', true);
      this._element.setAttribute('role', 'dialog');
      this._element.scrollTop = 0;
      const modalBody = SelectorEngine.findOne(SELECTOR_MODAL_BODY, this._dialog);
      if (modalBody) {
        modalBody.scrollTop = 0;
      }
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_SHOW$4);
      const transitionComplete = () => {
        if (this._config.focus) {
          this._focustrap.activate();
        }
        this._isTransitioning = false;
        EventHandler.trigger(this._element, EVENT_SHOWN$4, {
          relatedTarget
        });
      };
      this._queueCallback(transitionComplete, this._dialog, this._isAnimated());
    }
    _addEventListeners() {
      EventHandler.on(this._element, EVENT_KEYDOWN_DISMISS$1, event => {
        if (event.key !== ESCAPE_KEY$1) {
          return;
        }
        if (this._config.keyboard) {
          this.hide();
          return;
        }
        this._triggerBackdropTransition();
      });
      EventHandler.on(window, EVENT_RESIZE$1, () => {
        if (this._isShown && !this._isTransitioning) {
          this._adjustDialog();
        }
      });
      EventHandler.on(this._element, EVENT_MOUSEDOWN_DISMISS, event => {
        // a bad trick to segregate clicks that may start inside dialog but end outside, and avoid listen to scrollbar clicks
        EventHandler.one(this._element, EVENT_CLICK_DISMISS, event2 => {
          if (this._element !== event.target || this._element !== event2.target) {
            return;
          }
          if (this._config.backdrop === 'static') {
            this._triggerBackdropTransition();
            return;
          }
          if (this._config.backdrop) {
            this.hide();
          }
        });
      });
    }
    _hideModal() {
      this._element.style.display = 'none';
      this._element.setAttribute('aria-hidden', true);
      this._element.removeAttribute('aria-modal');
      this._element.removeAttribute('role');
      this._isTransitioning = false;
      this._backdrop.hide(() => {
        document.body.classList.remove(CLASS_NAME_OPEN);
        this._resetAdjustments();
        this._scrollBar.reset();
        EventHandler.trigger(this._element, EVENT_HIDDEN$4);
      });
    }
    _isAnimated() {
      return this._element.classList.contains(CLASS_NAME_FADE$3);
    }
    _triggerBackdropTransition() {
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED$1);
      if (hideEvent.defaultPrevented) {
        return;
      }
      const isModalOverflowing = this._element.scrollHeight > document.documentElement.clientHeight;
      const initialOverflowY = this._element.style.overflowY;
      // return if the following background transition hasn't yet completed
      if (initialOverflowY === 'hidden' || this._element.classList.contains(CLASS_NAME_STATIC)) {
        return;
      }
      if (!isModalOverflowing) {
        this._element.style.overflowY = 'hidden';
      }
      this._element.classList.add(CLASS_NAME_STATIC);
      this._queueCallback(() => {
        this._element.classList.remove(CLASS_NAME_STATIC);
        this._queueCallback(() => {
          this._element.style.overflowY = initialOverflowY;
        }, this._dialog);
      }, this._dialog);
      this._element.focus();
    }

    /**
     * The following methods are used to handle overflowing modals
     */

    _adjustDialog() {
      const isModalOverflowing = this._element.scrollHeight > document.documentElement.clientHeight;
      const scrollbarWidth = this._scrollBar.getWidth();
      const isBodyOverflowing = scrollbarWidth > 0;
      if (isBodyOverflowing && !isModalOverflowing) {
        const property = isRTL() ? 'paddingLeft' : 'paddingRight';
        this._element.style[property] = `${scrollbarWidth}px`;
      }
      if (!isBodyOverflowing && isModalOverflowing) {
        const property = isRTL() ? 'paddingRight' : 'paddingLeft';
        this._element.style[property] = `${scrollbarWidth}px`;
      }
    }
    _resetAdjustments() {
      this._element.style.paddingLeft = '';
      this._element.style.paddingRight = '';
    }

    // Static
    static jQueryInterface(config, relatedTarget) {
      return this.each(function () {
        const data = Modal.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](relatedTarget);
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$2, SELECTOR_DATA_TOGGLE$2, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    EventHandler.one(target, EVENT_SHOW$4, showEvent => {
      if (showEvent.defaultPrevented) {
        // only register focus restorer if modal will actually get shown
        return;
      }
      EventHandler.one(target, EVENT_HIDDEN$4, () => {
        if (isVisible(this)) {
          this.focus();
        }
      });
    });

    // avoid conflict when clicking modal toggler while another one is open
    const alreadyOpen = SelectorEngine.findOne(OPEN_SELECTOR$1);
    if (alreadyOpen) {
      Modal.getInstance(alreadyOpen).hide();
    }
    const data = Modal.getOrCreateInstance(target);
    data.toggle(this);
  });
  enableDismissTrigger(Modal);

  /**
   * jQuery
   */

  defineJQueryPlugin(Modal);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap offcanvas.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$6 = 'offcanvas';
  const DATA_KEY$3 = 'bs.offcanvas';
  const EVENT_KEY$3 = `.${DATA_KEY$3}`;
  const DATA_API_KEY$1 = '.data-api';
  const EVENT_LOAD_DATA_API$2 = `load${EVENT_KEY$3}${DATA_API_KEY$1}`;
  const ESCAPE_KEY = 'Escape';
  const CLASS_NAME_SHOW$3 = 'show';
  const CLASS_NAME_SHOWING$1 = 'showing';
  const CLASS_NAME_HIDING = 'hiding';
  const CLASS_NAME_BACKDROP = 'offcanvas-backdrop';
  const OPEN_SELECTOR = '.offcanvas.show';
  const EVENT_SHOW$3 = `show${EVENT_KEY$3}`;
  const EVENT_SHOWN$3 = `shown${EVENT_KEY$3}`;
  const EVENT_HIDE$3 = `hide${EVENT_KEY$3}`;
  const EVENT_HIDE_PREVENTED = `hidePrevented${EVENT_KEY$3}`;
  const EVENT_HIDDEN$3 = `hidden${EVENT_KEY$3}`;
  const EVENT_RESIZE = `resize${EVENT_KEY$3}`;
  const EVENT_CLICK_DATA_API$1 = `click${EVENT_KEY$3}${DATA_API_KEY$1}`;
  const EVENT_KEYDOWN_DISMISS = `keydown.dismiss${EVENT_KEY$3}`;
  const SELECTOR_DATA_TOGGLE$1 = '[data-bs-toggle="offcanvas"]';
  const Default$5 = {
    backdrop: true,
    keyboard: true,
    scroll: false
  };
  const DefaultType$5 = {
    backdrop: '(boolean|string)',
    keyboard: 'boolean',
    scroll: 'boolean'
  };

  /**
   * Class definition
   */

  class Offcanvas extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._isShown = false;
      this._backdrop = this._initializeBackDrop();
      this._focustrap = this._initializeFocusTrap();
      this._addEventListeners();
    }

    // Getters
    static get Default() {
      return Default$5;
    }
    static get DefaultType() {
      return DefaultType$5;
    }
    static get NAME() {
      return NAME$6;
    }

    // Public
    toggle(relatedTarget) {
      return this._isShown ? this.hide() : this.show(relatedTarget);
    }
    show(relatedTarget) {
      if (this._isShown) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW$3, {
        relatedTarget
      });
      if (showEvent.defaultPrevented) {
        return;
      }
      this._isShown = true;
      this._backdrop.show();
      if (!this._config.scroll) {
        new ScrollBarHelper().hide();
      }
      this._element.setAttribute('aria-modal', true);
      this._element.setAttribute('role', 'dialog');
      this._element.classList.add(CLASS_NAME_SHOWING$1);
      const completeCallBack = () => {
        if (!this._config.scroll || this._config.backdrop) {
          this._focustrap.activate();
        }
        this._element.classList.add(CLASS_NAME_SHOW$3);
        this._element.classList.remove(CLASS_NAME_SHOWING$1);
        EventHandler.trigger(this._element, EVENT_SHOWN$3, {
          relatedTarget
        });
      };
      this._queueCallback(completeCallBack, this._element, true);
    }
    hide() {
      if (!this._isShown) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE$3);
      if (hideEvent.defaultPrevented) {
        return;
      }
      this._focustrap.deactivate();
      this._element.blur();
      this._isShown = false;
      this._element.classList.add(CLASS_NAME_HIDING);
      this._backdrop.hide();
      const completeCallback = () => {
        this._element.classList.remove(CLASS_NAME_SHOW$3, CLASS_NAME_HIDING);
        this._element.removeAttribute('aria-modal');
        this._element.removeAttribute('role');
        if (!this._config.scroll) {
          new ScrollBarHelper().reset();
        }
        EventHandler.trigger(this._element, EVENT_HIDDEN$3);
      };
      this._queueCallback(completeCallback, this._element, true);
    }
    dispose() {
      this._backdrop.dispose();
      this._focustrap.deactivate();
      super.dispose();
    }

    // Private
    _initializeBackDrop() {
      const clickCallback = () => {
        if (this._config.backdrop === 'static') {
          EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED);
          return;
        }
        this.hide();
      };

      // 'static' option will be translated to true, and booleans will keep their value
      const isVisible = Boolean(this._config.backdrop);
      return new Backdrop({
        className: CLASS_NAME_BACKDROP,
        isVisible,
        isAnimated: true,
        rootElement: this._element.parentNode,
        clickCallback: isVisible ? clickCallback : null
      });
    }
    _initializeFocusTrap() {
      return new FocusTrap({
        trapElement: this._element
      });
    }
    _addEventListeners() {
      EventHandler.on(this._element, EVENT_KEYDOWN_DISMISS, event => {
        if (event.key !== ESCAPE_KEY) {
          return;
        }
        if (this._config.keyboard) {
          this.hide();
          return;
        }
        EventHandler.trigger(this._element, EVENT_HIDE_PREVENTED);
      });
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Offcanvas.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config](this);
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API$1, SELECTOR_DATA_TOGGLE$1, function (event) {
    const target = SelectorEngine.getElementFromSelector(this);
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    if (isDisabled(this)) {
      return;
    }
    EventHandler.one(target, EVENT_HIDDEN$3, () => {
      // focus on trigger when it is closed
      if (isVisible(this)) {
        this.focus();
      }
    });

    // avoid conflict when clicking a toggler of an offcanvas, while another is open
    const alreadyOpen = SelectorEngine.findOne(OPEN_SELECTOR);
    if (alreadyOpen && alreadyOpen !== target) {
      Offcanvas.getInstance(alreadyOpen).hide();
    }
    const data = Offcanvas.getOrCreateInstance(target);
    data.toggle(this);
  });
  EventHandler.on(window, EVENT_LOAD_DATA_API$2, () => {
    for (const selector of SelectorEngine.find(OPEN_SELECTOR)) {
      Offcanvas.getOrCreateInstance(selector).show();
    }
  });
  EventHandler.on(window, EVENT_RESIZE, () => {
    for (const element of SelectorEngine.find('[aria-modal][class*=show][class*=offcanvas-]')) {
      if (getComputedStyle(element).position !== 'fixed') {
        Offcanvas.getOrCreateInstance(element).hide();
      }
    }
  });
  enableDismissTrigger(Offcanvas);

  /**
   * jQuery
   */

  defineJQueryPlugin(Offcanvas);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/sanitizer.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  // js-docs-start allow-list
  const ARIA_ATTRIBUTE_PATTERN = /^aria-[\w-]*$/i;
  const DefaultAllowlist = {
    // Global attributes allowed on any supplied element below.
    '*': ['class', 'dir', 'id', 'lang', 'role', ARIA_ATTRIBUTE_PATTERN],
    a: ['target', 'href', 'title', 'rel'],
    area: [],
    b: [],
    br: [],
    col: [],
    code: [],
    dd: [],
    div: [],
    dl: [],
    dt: [],
    em: [],
    hr: [],
    h1: [],
    h2: [],
    h3: [],
    h4: [],
    h5: [],
    h6: [],
    i: [],
    img: ['src', 'srcset', 'alt', 'title', 'width', 'height'],
    li: [],
    ol: [],
    p: [],
    pre: [],
    s: [],
    small: [],
    span: [],
    sub: [],
    sup: [],
    strong: [],
    u: [],
    ul: []
  };
  // js-docs-end allow-list

  const uriAttributes = new Set(['background', 'cite', 'href', 'itemtype', 'longdesc', 'poster', 'src', 'xlink:href']);

  /**
   * A pattern that recognizes URLs that are safe wrt. XSS in URL navigation
   * contexts.
   *
   * Shout-out to Angular https://github.com/angular/angular/blob/15.2.8/packages/core/src/sanitization/url_sanitizer.ts#L38
   */
  // eslint-disable-next-line unicorn/better-regex
  const SAFE_URL_PATTERN = /^(?!javascript:)(?:[a-z0-9+.-]+:|[^&:/?#]*(?:[/?#]|$))/i;
  const allowedAttribute = (attribute, allowedAttributeList) => {
    const attributeName = attribute.nodeName.toLowerCase();
    if (allowedAttributeList.includes(attributeName)) {
      if (uriAttributes.has(attributeName)) {
        return Boolean(SAFE_URL_PATTERN.test(attribute.nodeValue));
      }
      return true;
    }

    // Check if a regular expression validates the attribute.
    return allowedAttributeList.filter(attributeRegex => attributeRegex instanceof RegExp).some(regex => regex.test(attributeName));
  };
  function sanitizeHtml(unsafeHtml, allowList, sanitizeFunction) {
    if (!unsafeHtml.length) {
      return unsafeHtml;
    }
    if (sanitizeFunction && typeof sanitizeFunction === 'function') {
      return sanitizeFunction(unsafeHtml);
    }
    const domParser = new window.DOMParser();
    const createdDocument = domParser.parseFromString(unsafeHtml, 'text/html');
    const elements = [].concat(...createdDocument.body.querySelectorAll('*'));
    for (const element of elements) {
      const elementName = element.nodeName.toLowerCase();
      if (!Object.keys(allowList).includes(elementName)) {
        element.remove();
        continue;
      }
      const attributeList = [].concat(...element.attributes);
      const allowedAttributes = [].concat(allowList['*'] || [], allowList[elementName] || []);
      for (const attribute of attributeList) {
        if (!allowedAttribute(attribute, allowedAttributes)) {
          element.removeAttribute(attribute.nodeName);
        }
      }
    }
    return createdDocument.body.innerHTML;
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap util/template-factory.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$5 = 'TemplateFactory';
  const Default$4 = {
    allowList: DefaultAllowlist,
    content: {},
    // { selector : text ,  selector2 : text2 , }
    extraClass: '',
    html: false,
    sanitize: true,
    sanitizeFn: null,
    template: '<div></div>'
  };
  const DefaultType$4 = {
    allowList: 'object',
    content: 'object',
    extraClass: '(string|function)',
    html: 'boolean',
    sanitize: 'boolean',
    sanitizeFn: '(null|function)',
    template: 'string'
  };
  const DefaultContentType = {
    entry: '(string|element|function|null)',
    selector: '(string|element)'
  };

  /**
   * Class definition
   */

  class TemplateFactory extends Config {
    constructor(config) {
      super();
      this._config = this._getConfig(config);
    }

    // Getters
    static get Default() {
      return Default$4;
    }
    static get DefaultType() {
      return DefaultType$4;
    }
    static get NAME() {
      return NAME$5;
    }

    // Public
    getContent() {
      return Object.values(this._config.content).map(config => this._resolvePossibleFunction(config)).filter(Boolean);
    }
    hasContent() {
      return this.getContent().length > 0;
    }
    changeContent(content) {
      this._checkContent(content);
      this._config.content = {
        ...this._config.content,
        ...content
      };
      return this;
    }
    toHtml() {
      const templateWrapper = document.createElement('div');
      templateWrapper.innerHTML = this._maybeSanitize(this._config.template);
      for (const [selector, text] of Object.entries(this._config.content)) {
        this._setContent(templateWrapper, text, selector);
      }
      const template = templateWrapper.children[0];
      const extraClass = this._resolvePossibleFunction(this._config.extraClass);
      if (extraClass) {
        template.classList.add(...extraClass.split(' '));
      }
      return template;
    }

    // Private
    _typeCheckConfig(config) {
      super._typeCheckConfig(config);
      this._checkContent(config.content);
    }
    _checkContent(arg) {
      for (const [selector, content] of Object.entries(arg)) {
        super._typeCheckConfig({
          selector,
          entry: content
        }, DefaultContentType);
      }
    }
    _setContent(template, content, selector) {
      const templateElement = SelectorEngine.findOne(selector, template);
      if (!templateElement) {
        return;
      }
      content = this._resolvePossibleFunction(content);
      if (!content) {
        templateElement.remove();
        return;
      }
      if (isElement$1(content)) {
        this._putElementInTemplate(getElement(content), templateElement);
        return;
      }
      if (this._config.html) {
        templateElement.innerHTML = this._maybeSanitize(content);
        return;
      }
      templateElement.textContent = content;
    }
    _maybeSanitize(arg) {
      return this._config.sanitize ? sanitizeHtml(arg, this._config.allowList, this._config.sanitizeFn) : arg;
    }
    _resolvePossibleFunction(arg) {
      return execute(arg, [this]);
    }
    _putElementInTemplate(element, templateElement) {
      if (this._config.html) {
        templateElement.innerHTML = '';
        templateElement.append(element);
        return;
      }
      templateElement.textContent = element.textContent;
    }
  }

  /**
   * --------------------------------------------------------------------------
   * Bootstrap tooltip.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$4 = 'tooltip';
  const DISALLOWED_ATTRIBUTES = new Set(['sanitize', 'allowList', 'sanitizeFn']);
  const CLASS_NAME_FADE$2 = 'fade';
  const CLASS_NAME_MODAL = 'modal';
  const CLASS_NAME_SHOW$2 = 'show';
  const SELECTOR_TOOLTIP_INNER = '.tooltip-inner';
  const SELECTOR_MODAL = `.${CLASS_NAME_MODAL}`;
  const EVENT_MODAL_HIDE = 'hide.bs.modal';
  const TRIGGER_HOVER = 'hover';
  const TRIGGER_FOCUS = 'focus';
  const TRIGGER_CLICK = 'click';
  const TRIGGER_MANUAL = 'manual';
  const EVENT_HIDE$2 = 'hide';
  const EVENT_HIDDEN$2 = 'hidden';
  const EVENT_SHOW$2 = 'show';
  const EVENT_SHOWN$2 = 'shown';
  const EVENT_INSERTED = 'inserted';
  const EVENT_CLICK$1 = 'click';
  const EVENT_FOCUSIN$1 = 'focusin';
  const EVENT_FOCUSOUT$1 = 'focusout';
  const EVENT_MOUSEENTER = 'mouseenter';
  const EVENT_MOUSELEAVE = 'mouseleave';
  const AttachmentMap = {
    AUTO: 'auto',
    TOP: 'top',
    RIGHT: isRTL() ? 'left' : 'right',
    BOTTOM: 'bottom',
    LEFT: isRTL() ? 'right' : 'left'
  };
  const Default$3 = {
    allowList: DefaultAllowlist,
    animation: true,
    boundary: 'clippingParents',
    container: false,
    customClass: '',
    delay: 0,
    fallbackPlacements: ['top', 'right', 'bottom', 'left'],
    html: false,
    offset: [0, 6],
    placement: 'top',
    popperConfig: null,
    sanitize: true,
    sanitizeFn: null,
    selector: false,
    template: '<div class="tooltip" role="tooltip">' + '<div class="tooltip-arrow"></div>' + '<div class="tooltip-inner"></div>' + '</div>',
    title: '',
    trigger: 'hover focus'
  };
  const DefaultType$3 = {
    allowList: 'object',
    animation: 'boolean',
    boundary: '(string|element)',
    container: '(string|element|boolean)',
    customClass: '(string|function)',
    delay: '(number|object)',
    fallbackPlacements: 'array',
    html: 'boolean',
    offset: '(array|string|function)',
    placement: '(string|function)',
    popperConfig: '(null|object|function)',
    sanitize: 'boolean',
    sanitizeFn: '(null|function)',
    selector: '(string|boolean)',
    template: 'string',
    title: '(string|element|function)',
    trigger: 'string'
  };

  /**
   * Class definition
   */

  class Tooltip extends BaseComponent {
    constructor(element, config) {
      if (typeof Popper === 'undefined') {
        throw new TypeError('Bootstrap\'s tooltips require Popper (https://popper.js.org)');
      }
      super(element, config);

      // Private
      this._isEnabled = true;
      this._timeout = 0;
      this._isHovered = null;
      this._activeTrigger = {};
      this._popper = null;
      this._templateFactory = null;
      this._newContent = null;

      // Protected
      this.tip = null;
      this._setListeners();
      if (!this._config.selector) {
        this._fixTitle();
      }
    }

    // Getters
    static get Default() {
      return Default$3;
    }
    static get DefaultType() {
      return DefaultType$3;
    }
    static get NAME() {
      return NAME$4;
    }

    // Public
    enable() {
      this._isEnabled = true;
    }
    disable() {
      this._isEnabled = false;
    }
    toggleEnabled() {
      this._isEnabled = !this._isEnabled;
    }
    toggle() {
      if (!this._isEnabled) {
        return;
      }
      this._activeTrigger.click = !this._activeTrigger.click;
      if (this._isShown()) {
        this._leave();
        return;
      }
      this._enter();
    }
    dispose() {
      clearTimeout(this._timeout);
      EventHandler.off(this._element.closest(SELECTOR_MODAL), EVENT_MODAL_HIDE, this._hideModalHandler);
      if (this._element.getAttribute('data-bs-original-title')) {
        this._element.setAttribute('title', this._element.getAttribute('data-bs-original-title'));
      }
      this._disposePopper();
      super.dispose();
    }
    show() {
      if (this._element.style.display === 'none') {
        throw new Error('Please use show on visible elements');
      }
      if (!(this._isWithContent() && this._isEnabled)) {
        return;
      }
      const showEvent = EventHandler.trigger(this._element, this.constructor.eventName(EVENT_SHOW$2));
      const shadowRoot = findShadowRoot(this._element);
      const isInTheDom = (shadowRoot || this._element.ownerDocument.documentElement).contains(this._element);
      if (showEvent.defaultPrevented || !isInTheDom) {
        return;
      }

      // TODO: v6 remove this or make it optional
      this._disposePopper();
      const tip = this._getTipElement();
      this._element.setAttribute('aria-describedby', tip.getAttribute('id'));
      const {
        container
      } = this._config;
      if (!this._element.ownerDocument.documentElement.contains(this.tip)) {
        container.append(tip);
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_INSERTED));
      }
      this._popper = this._createPopper(tip);
      tip.classList.add(CLASS_NAME_SHOW$2);

      // If this is a touch-enabled device we add extra
      // empty mouseover listeners to the body's immediate children;
      // only needed because of broken event delegation on iOS
      // https://www.quirksmode.org/blog/archives/2014/02/mouse_event_bub.html
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.on(element, 'mouseover', noop);
        }
      }
      const complete = () => {
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_SHOWN$2));
        if (this._isHovered === false) {
          this._leave();
        }
        this._isHovered = false;
      };
      this._queueCallback(complete, this.tip, this._isAnimated());
    }
    hide() {
      if (!this._isShown()) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, this.constructor.eventName(EVENT_HIDE$2));
      if (hideEvent.defaultPrevented) {
        return;
      }
      const tip = this._getTipElement();
      tip.classList.remove(CLASS_NAME_SHOW$2);

      // If this is a touch-enabled device we remove the extra
      // empty mouseover listeners we added for iOS support
      if ('ontouchstart' in document.documentElement) {
        for (const element of [].concat(...document.body.children)) {
          EventHandler.off(element, 'mouseover', noop);
        }
      }
      this._activeTrigger[TRIGGER_CLICK] = false;
      this._activeTrigger[TRIGGER_FOCUS] = false;
      this._activeTrigger[TRIGGER_HOVER] = false;
      this._isHovered = null; // it is a trick to support manual triggering

      const complete = () => {
        if (this._isWithActiveTrigger()) {
          return;
        }
        if (!this._isHovered) {
          this._disposePopper();
        }
        this._element.removeAttribute('aria-describedby');
        EventHandler.trigger(this._element, this.constructor.eventName(EVENT_HIDDEN$2));
      };
      this._queueCallback(complete, this.tip, this._isAnimated());
    }
    update() {
      if (this._popper) {
        this._popper.update();
      }
    }

    // Protected
    _isWithContent() {
      return Boolean(this._getTitle());
    }
    _getTipElement() {
      if (!this.tip) {
        this.tip = this._createTipElement(this._newContent || this._getContentForTemplate());
      }
      return this.tip;
    }
    _createTipElement(content) {
      const tip = this._getTemplateFactory(content).toHtml();

      // TODO: remove this check in v6
      if (!tip) {
        return null;
      }
      tip.classList.remove(CLASS_NAME_FADE$2, CLASS_NAME_SHOW$2);
      // TODO: v6 the following can be achieved with CSS only
      tip.classList.add(`bs-${this.constructor.NAME}-auto`);
      const tipId = getUID(this.constructor.NAME).toString();
      tip.setAttribute('id', tipId);
      if (this._isAnimated()) {
        tip.classList.add(CLASS_NAME_FADE$2);
      }
      return tip;
    }
    setContent(content) {
      this._newContent = content;
      if (this._isShown()) {
        this._disposePopper();
        this.show();
      }
    }
    _getTemplateFactory(content) {
      if (this._templateFactory) {
        this._templateFactory.changeContent(content);
      } else {
        this._templateFactory = new TemplateFactory({
          ...this._config,
          // the `content` var has to be after `this._config`
          // to override config.content in case of popover
          content,
          extraClass: this._resolvePossibleFunction(this._config.customClass)
        });
      }
      return this._templateFactory;
    }
    _getContentForTemplate() {
      return {
        [SELECTOR_TOOLTIP_INNER]: this._getTitle()
      };
    }
    _getTitle() {
      return this._resolvePossibleFunction(this._config.title) || this._element.getAttribute('data-bs-original-title');
    }

    // Private
    _initializeOnDelegatedTarget(event) {
      return this.constructor.getOrCreateInstance(event.delegateTarget, this._getDelegateConfig());
    }
    _isAnimated() {
      return this._config.animation || this.tip && this.tip.classList.contains(CLASS_NAME_FADE$2);
    }
    _isShown() {
      return this.tip && this.tip.classList.contains(CLASS_NAME_SHOW$2);
    }
    _createPopper(tip) {
      const placement = execute(this._config.placement, [this, tip, this._element]);
      const attachment = AttachmentMap[placement.toUpperCase()];
      return createPopper(this._element, tip, this._getPopperConfig(attachment));
    }
    _getOffset() {
      const {
        offset
      } = this._config;
      if (typeof offset === 'string') {
        return offset.split(',').map(value => Number.parseInt(value, 10));
      }
      if (typeof offset === 'function') {
        return popperData => offset(popperData, this._element);
      }
      return offset;
    }
    _resolvePossibleFunction(arg) {
      return execute(arg, [this._element]);
    }
    _getPopperConfig(attachment) {
      const defaultBsPopperConfig = {
        placement: attachment,
        modifiers: [{
          name: 'flip',
          options: {
            fallbackPlacements: this._config.fallbackPlacements
          }
        }, {
          name: 'offset',
          options: {
            offset: this._getOffset()
          }
        }, {
          name: 'preventOverflow',
          options: {
            boundary: this._config.boundary
          }
        }, {
          name: 'arrow',
          options: {
            element: `.${this.constructor.NAME}-arrow`
          }
        }, {
          name: 'preSetPlacement',
          enabled: true,
          phase: 'beforeMain',
          fn: data => {
            // Pre-set Popper's placement attribute in order to read the arrow sizes properly.
            // Otherwise, Popper mixes up the width and height dimensions since the initial arrow style is for top placement
            this._getTipElement().setAttribute('data-popper-placement', data.state.placement);
          }
        }]
      };
      return {
        ...defaultBsPopperConfig,
        ...execute(this._config.popperConfig, [defaultBsPopperConfig])
      };
    }
    _setListeners() {
      const triggers = this._config.trigger.split(' ');
      for (const trigger of triggers) {
        if (trigger === 'click') {
          EventHandler.on(this._element, this.constructor.eventName(EVENT_CLICK$1), this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context.toggle();
          });
        } else if (trigger !== TRIGGER_MANUAL) {
          const eventIn = trigger === TRIGGER_HOVER ? this.constructor.eventName(EVENT_MOUSEENTER) : this.constructor.eventName(EVENT_FOCUSIN$1);
          const eventOut = trigger === TRIGGER_HOVER ? this.constructor.eventName(EVENT_MOUSELEAVE) : this.constructor.eventName(EVENT_FOCUSOUT$1);
          EventHandler.on(this._element, eventIn, this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context._activeTrigger[event.type === 'focusin' ? TRIGGER_FOCUS : TRIGGER_HOVER] = true;
            context._enter();
          });
          EventHandler.on(this._element, eventOut, this._config.selector, event => {
            const context = this._initializeOnDelegatedTarget(event);
            context._activeTrigger[event.type === 'focusout' ? TRIGGER_FOCUS : TRIGGER_HOVER] = context._element.contains(event.relatedTarget);
            context._leave();
          });
        }
      }
      this._hideModalHandler = () => {
        if (this._element) {
          this.hide();
        }
      };
      EventHandler.on(this._element.closest(SELECTOR_MODAL), EVENT_MODAL_HIDE, this._hideModalHandler);
    }
    _fixTitle() {
      const title = this._element.getAttribute('title');
      if (!title) {
        return;
      }
      if (!this._element.getAttribute('aria-label') && !this._element.textContent.trim()) {
        this._element.setAttribute('aria-label', title);
      }
      this._element.setAttribute('data-bs-original-title', title); // DO NOT USE IT. Is only for backwards compatibility
      this._element.removeAttribute('title');
    }
    _enter() {
      if (this._isShown() || this._isHovered) {
        this._isHovered = true;
        return;
      }
      this._isHovered = true;
      this._setTimeout(() => {
        if (this._isHovered) {
          this.show();
        }
      }, this._config.delay.show);
    }
    _leave() {
      if (this._isWithActiveTrigger()) {
        return;
      }
      this._isHovered = false;
      this._setTimeout(() => {
        if (!this._isHovered) {
          this.hide();
        }
      }, this._config.delay.hide);
    }
    _setTimeout(handler, timeout) {
      clearTimeout(this._timeout);
      this._timeout = setTimeout(handler, timeout);
    }
    _isWithActiveTrigger() {
      return Object.values(this._activeTrigger).includes(true);
    }
    _getConfig(config) {
      const dataAttributes = Manipulator.getDataAttributes(this._element);
      for (const dataAttribute of Object.keys(dataAttributes)) {
        if (DISALLOWED_ATTRIBUTES.has(dataAttribute)) {
          delete dataAttributes[dataAttribute];
        }
      }
      config = {
        ...dataAttributes,
        ...(typeof config === 'object' && config ? config : {})
      };
      config = this._mergeConfigObj(config);
      config = this._configAfterMerge(config);
      this._typeCheckConfig(config);
      return config;
    }
    _configAfterMerge(config) {
      config.container = config.container === false ? document.body : getElement(config.container);
      if (typeof config.delay === 'number') {
        config.delay = {
          show: config.delay,
          hide: config.delay
        };
      }
      if (typeof config.title === 'number') {
        config.title = config.title.toString();
      }
      if (typeof config.content === 'number') {
        config.content = config.content.toString();
      }
      return config;
    }
    _getDelegateConfig() {
      const config = {};
      for (const [key, value] of Object.entries(this._config)) {
        if (this.constructor.Default[key] !== value) {
          config[key] = value;
        }
      }
      config.selector = false;
      config.trigger = 'manual';

      // In the future can be replaced with:
      // const keysWithDifferentValues = Object.entries(this._config).filter(entry => this.constructor.Default[entry[0]] !== this._config[entry[0]])
      // `Object.fromEntries(keysWithDifferentValues)`
      return config;
    }
    _disposePopper() {
      if (this._popper) {
        this._popper.destroy();
        this._popper = null;
      }
      if (this.tip) {
        this.tip.remove();
        this.tip = null;
      }
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Tooltip.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * jQuery
   */

  defineJQueryPlugin(Tooltip);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap popover.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$3 = 'popover';
  const SELECTOR_TITLE = '.popover-header';
  const SELECTOR_CONTENT = '.popover-body';
  const Default$2 = {
    ...Tooltip.Default,
    content: '',
    offset: [0, 8],
    placement: 'right',
    template: '<div class="popover" role="tooltip">' + '<div class="popover-arrow"></div>' + '<h3 class="popover-header"></h3>' + '<div class="popover-body"></div>' + '</div>',
    trigger: 'click'
  };
  const DefaultType$2 = {
    ...Tooltip.DefaultType,
    content: '(null|string|element|function)'
  };

  /**
   * Class definition
   */

  class Popover extends Tooltip {
    // Getters
    static get Default() {
      return Default$2;
    }
    static get DefaultType() {
      return DefaultType$2;
    }
    static get NAME() {
      return NAME$3;
    }

    // Overrides
    _isWithContent() {
      return this._getTitle() || this._getContent();
    }

    // Private
    _getContentForTemplate() {
      return {
        [SELECTOR_TITLE]: this._getTitle(),
        [SELECTOR_CONTENT]: this._getContent()
      };
    }
    _getContent() {
      return this._resolvePossibleFunction(this._config.content);
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Popover.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (typeof data[config] === 'undefined') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * jQuery
   */

  defineJQueryPlugin(Popover);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap scrollspy.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$2 = 'scrollspy';
  const DATA_KEY$2 = 'bs.scrollspy';
  const EVENT_KEY$2 = `.${DATA_KEY$2}`;
  const DATA_API_KEY = '.data-api';
  const EVENT_ACTIVATE = `activate${EVENT_KEY$2}`;
  const EVENT_CLICK = `click${EVENT_KEY$2}`;
  const EVENT_LOAD_DATA_API$1 = `load${EVENT_KEY$2}${DATA_API_KEY}`;
  const CLASS_NAME_DROPDOWN_ITEM = 'dropdown-item';
  const CLASS_NAME_ACTIVE$1 = 'active';
  const SELECTOR_DATA_SPY = '[data-bs-spy="scroll"]';
  const SELECTOR_TARGET_LINKS = '[href]';
  const SELECTOR_NAV_LIST_GROUP = '.nav, .list-group';
  const SELECTOR_NAV_LINKS = '.nav-link';
  const SELECTOR_NAV_ITEMS = '.nav-item';
  const SELECTOR_LIST_ITEMS = '.list-group-item';
  const SELECTOR_LINK_ITEMS = `${SELECTOR_NAV_LINKS}, ${SELECTOR_NAV_ITEMS} > ${SELECTOR_NAV_LINKS}, ${SELECTOR_LIST_ITEMS}`;
  const SELECTOR_DROPDOWN = '.dropdown';
  const SELECTOR_DROPDOWN_TOGGLE$1 = '.dropdown-toggle';
  const Default$1 = {
    offset: null,
    // TODO: v6 @deprecated, keep it for backwards compatibility reasons
    rootMargin: '0px 0px -25%',
    smoothScroll: false,
    target: null,
    threshold: [0.1, 0.5, 1]
  };
  const DefaultType$1 = {
    offset: '(number|null)',
    // TODO v6 @deprecated, keep it for backwards compatibility reasons
    rootMargin: 'string',
    smoothScroll: 'boolean',
    target: 'element',
    threshold: 'array'
  };

  /**
   * Class definition
   */

  class ScrollSpy extends BaseComponent {
    constructor(element, config) {
      super(element, config);

      // this._element is the observablesContainer and config.target the menu links wrapper
      this._targetLinks = new Map();
      this._observableSections = new Map();
      this._rootElement = getComputedStyle(this._element).overflowY === 'visible' ? null : this._element;
      this._activeTarget = null;
      this._observer = null;
      this._previousScrollData = {
        visibleEntryTop: 0,
        parentScrollTop: 0
      };
      this.refresh(); // initialize
    }

    // Getters
    static get Default() {
      return Default$1;
    }
    static get DefaultType() {
      return DefaultType$1;
    }
    static get NAME() {
      return NAME$2;
    }

    // Public
    refresh() {
      this._initializeTargetsAndObservables();
      this._maybeEnableSmoothScroll();
      if (this._observer) {
        this._observer.disconnect();
      } else {
        this._observer = this._getNewObserver();
      }
      for (const section of this._observableSections.values()) {
        this._observer.observe(section);
      }
    }
    dispose() {
      this._observer.disconnect();
      super.dispose();
    }

    // Private
    _configAfterMerge(config) {
      // TODO: on v6 target should be given explicitly & remove the {target: 'ss-target'} case
      config.target = getElement(config.target) || document.body;

      // TODO: v6 Only for backwards compatibility reasons. Use rootMargin only
      config.rootMargin = config.offset ? `${config.offset}px 0px -30%` : config.rootMargin;
      if (typeof config.threshold === 'string') {
        config.threshold = config.threshold.split(',').map(value => Number.parseFloat(value));
      }
      return config;
    }
    _maybeEnableSmoothScroll() {
      if (!this._config.smoothScroll) {
        return;
      }

      // unregister any previous listeners
      EventHandler.off(this._config.target, EVENT_CLICK);
      EventHandler.on(this._config.target, EVENT_CLICK, SELECTOR_TARGET_LINKS, event => {
        const observableSection = this._observableSections.get(event.target.hash);
        if (observableSection) {
          event.preventDefault();
          const root = this._rootElement || window;
          const height = observableSection.offsetTop - this._element.offsetTop;
          if (root.scrollTo) {
            root.scrollTo({
              top: height,
              behavior: 'smooth'
            });
            return;
          }

          // Chrome 60 doesn't support `scrollTo`
          root.scrollTop = height;
        }
      });
    }
    _getNewObserver() {
      const options = {
        root: this._rootElement,
        threshold: this._config.threshold,
        rootMargin: this._config.rootMargin
      };
      return new IntersectionObserver(entries => this._observerCallback(entries), options);
    }

    // The logic of selection
    _observerCallback(entries) {
      const targetElement = entry => this._targetLinks.get(`#${entry.target.id}`);
      const activate = entry => {
        this._previousScrollData.visibleEntryTop = entry.target.offsetTop;
        this._process(targetElement(entry));
      };
      const parentScrollTop = (this._rootElement || document.documentElement).scrollTop;
      const userScrollsDown = parentScrollTop >= this._previousScrollData.parentScrollTop;
      this._previousScrollData.parentScrollTop = parentScrollTop;
      for (const entry of entries) {
        if (!entry.isIntersecting) {
          this._activeTarget = null;
          this._clearActiveClass(targetElement(entry));
          continue;
        }
        const entryIsLowerThanPrevious = entry.target.offsetTop >= this._previousScrollData.visibleEntryTop;
        // if we are scrolling down, pick the bigger offsetTop
        if (userScrollsDown && entryIsLowerThanPrevious) {
          activate(entry);
          // if parent isn't scrolled, let's keep the first visible item, breaking the iteration
          if (!parentScrollTop) {
            return;
          }
          continue;
        }

        // if we are scrolling up, pick the smallest offsetTop
        if (!userScrollsDown && !entryIsLowerThanPrevious) {
          activate(entry);
        }
      }
    }
    _initializeTargetsAndObservables() {
      this._targetLinks = new Map();
      this._observableSections = new Map();
      const targetLinks = SelectorEngine.find(SELECTOR_TARGET_LINKS, this._config.target);
      for (const anchor of targetLinks) {
        // ensure that the anchor has an id and is not disabled
        if (!anchor.hash || isDisabled(anchor)) {
          continue;
        }
        const observableSection = SelectorEngine.findOne(decodeURI(anchor.hash), this._element);

        // ensure that the observableSection exists & is visible
        if (isVisible(observableSection)) {
          this._targetLinks.set(decodeURI(anchor.hash), anchor);
          this._observableSections.set(anchor.hash, observableSection);
        }
      }
    }
    _process(target) {
      if (this._activeTarget === target) {
        return;
      }
      this._clearActiveClass(this._config.target);
      this._activeTarget = target;
      target.classList.add(CLASS_NAME_ACTIVE$1);
      this._activateParents(target);
      EventHandler.trigger(this._element, EVENT_ACTIVATE, {
        relatedTarget: target
      });
    }
    _activateParents(target) {
      // Activate dropdown parents
      if (target.classList.contains(CLASS_NAME_DROPDOWN_ITEM)) {
        SelectorEngine.findOne(SELECTOR_DROPDOWN_TOGGLE$1, target.closest(SELECTOR_DROPDOWN)).classList.add(CLASS_NAME_ACTIVE$1);
        return;
      }
      for (const listGroup of SelectorEngine.parents(target, SELECTOR_NAV_LIST_GROUP)) {
        // Set triggered links parents as active
        // With both <ul> and <nav> markup a parent is the previous sibling of any nav ancestor
        for (const item of SelectorEngine.prev(listGroup, SELECTOR_LINK_ITEMS)) {
          item.classList.add(CLASS_NAME_ACTIVE$1);
        }
      }
    }
    _clearActiveClass(parent) {
      parent.classList.remove(CLASS_NAME_ACTIVE$1);
      const activeNodes = SelectorEngine.find(`${SELECTOR_TARGET_LINKS}.${CLASS_NAME_ACTIVE$1}`, parent);
      for (const node of activeNodes) {
        node.classList.remove(CLASS_NAME_ACTIVE$1);
      }
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = ScrollSpy.getOrCreateInstance(this, config);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(window, EVENT_LOAD_DATA_API$1, () => {
    for (const spy of SelectorEngine.find(SELECTOR_DATA_SPY)) {
      ScrollSpy.getOrCreateInstance(spy);
    }
  });

  /**
   * jQuery
   */

  defineJQueryPlugin(ScrollSpy);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap tab.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME$1 = 'tab';
  const DATA_KEY$1 = 'bs.tab';
  const EVENT_KEY$1 = `.${DATA_KEY$1}`;
  const EVENT_HIDE$1 = `hide${EVENT_KEY$1}`;
  const EVENT_HIDDEN$1 = `hidden${EVENT_KEY$1}`;
  const EVENT_SHOW$1 = `show${EVENT_KEY$1}`;
  const EVENT_SHOWN$1 = `shown${EVENT_KEY$1}`;
  const EVENT_CLICK_DATA_API = `click${EVENT_KEY$1}`;
  const EVENT_KEYDOWN = `keydown${EVENT_KEY$1}`;
  const EVENT_LOAD_DATA_API = `load${EVENT_KEY$1}`;
  const ARROW_LEFT_KEY = 'ArrowLeft';
  const ARROW_RIGHT_KEY = 'ArrowRight';
  const ARROW_UP_KEY = 'ArrowUp';
  const ARROW_DOWN_KEY = 'ArrowDown';
  const HOME_KEY = 'Home';
  const END_KEY = 'End';
  const CLASS_NAME_ACTIVE = 'active';
  const CLASS_NAME_FADE$1 = 'fade';
  const CLASS_NAME_SHOW$1 = 'show';
  const CLASS_DROPDOWN = 'dropdown';
  const SELECTOR_DROPDOWN_TOGGLE = '.dropdown-toggle';
  const SELECTOR_DROPDOWN_MENU = '.dropdown-menu';
  const NOT_SELECTOR_DROPDOWN_TOGGLE = `:not(${SELECTOR_DROPDOWN_TOGGLE})`;
  const SELECTOR_TAB_PANEL = '.list-group, .nav, [role="tablist"]';
  const SELECTOR_OUTER = '.nav-item, .list-group-item';
  const SELECTOR_INNER = `.nav-link${NOT_SELECTOR_DROPDOWN_TOGGLE}, .list-group-item${NOT_SELECTOR_DROPDOWN_TOGGLE}, [role="tab"]${NOT_SELECTOR_DROPDOWN_TOGGLE}`;
  const SELECTOR_DATA_TOGGLE = '[data-bs-toggle="tab"], [data-bs-toggle="pill"], [data-bs-toggle="list"]'; // TODO: could only be `tab` in v6
  const SELECTOR_INNER_ELEM = `${SELECTOR_INNER}, ${SELECTOR_DATA_TOGGLE}`;
  const SELECTOR_DATA_TOGGLE_ACTIVE = `.${CLASS_NAME_ACTIVE}[data-bs-toggle="tab"], .${CLASS_NAME_ACTIVE}[data-bs-toggle="pill"], .${CLASS_NAME_ACTIVE}[data-bs-toggle="list"]`;

  /**
   * Class definition
   */

  class Tab extends BaseComponent {
    constructor(element) {
      super(element);
      this._parent = this._element.closest(SELECTOR_TAB_PANEL);
      if (!this._parent) {
        return;
        // TODO: should throw exception in v6
        // throw new TypeError(`${element.outerHTML} has not a valid parent ${SELECTOR_INNER_ELEM}`)
      }

      // Set up initial aria attributes
      this._setInitialAttributes(this._parent, this._getChildren());
      EventHandler.on(this._element, EVENT_KEYDOWN, event => this._keydown(event));
    }

    // Getters
    static get NAME() {
      return NAME$1;
    }

    // Public
    show() {
      // Shows this elem and deactivate the active sibling if exists
      const innerElem = this._element;
      if (this._elemIsActive(innerElem)) {
        return;
      }

      // Search for active tab on same parent to deactivate it
      const active = this._getActiveElem();
      const hideEvent = active ? EventHandler.trigger(active, EVENT_HIDE$1, {
        relatedTarget: innerElem
      }) : null;
      const showEvent = EventHandler.trigger(innerElem, EVENT_SHOW$1, {
        relatedTarget: active
      });
      if (showEvent.defaultPrevented || hideEvent && hideEvent.defaultPrevented) {
        return;
      }
      this._deactivate(active, innerElem);
      this._activate(innerElem, active);
    }

    // Private
    _activate(element, relatedElem) {
      if (!element) {
        return;
      }
      element.classList.add(CLASS_NAME_ACTIVE);
      this._activate(SelectorEngine.getElementFromSelector(element)); // Search and activate/show the proper section

      const complete = () => {
        if (element.getAttribute('role') !== 'tab') {
          element.classList.add(CLASS_NAME_SHOW$1);
          return;
        }
        element.removeAttribute('tabindex');
        element.setAttribute('aria-selected', true);
        this._toggleDropDown(element, true);
        EventHandler.trigger(element, EVENT_SHOWN$1, {
          relatedTarget: relatedElem
        });
      };
      this._queueCallback(complete, element, element.classList.contains(CLASS_NAME_FADE$1));
    }
    _deactivate(element, relatedElem) {
      if (!element) {
        return;
      }
      element.classList.remove(CLASS_NAME_ACTIVE);
      element.blur();
      this._deactivate(SelectorEngine.getElementFromSelector(element)); // Search and deactivate the shown section too

      const complete = () => {
        if (element.getAttribute('role') !== 'tab') {
          element.classList.remove(CLASS_NAME_SHOW$1);
          return;
        }
        element.setAttribute('aria-selected', false);
        element.setAttribute('tabindex', '-1');
        this._toggleDropDown(element, false);
        EventHandler.trigger(element, EVENT_HIDDEN$1, {
          relatedTarget: relatedElem
        });
      };
      this._queueCallback(complete, element, element.classList.contains(CLASS_NAME_FADE$1));
    }
    _keydown(event) {
      if (![ARROW_LEFT_KEY, ARROW_RIGHT_KEY, ARROW_UP_KEY, ARROW_DOWN_KEY, HOME_KEY, END_KEY].includes(event.key)) {
        return;
      }
      event.stopPropagation(); // stopPropagation/preventDefault both added to support up/down keys without scrolling the page
      event.preventDefault();
      const children = this._getChildren().filter(element => !isDisabled(element));
      let nextActiveElement;
      if ([HOME_KEY, END_KEY].includes(event.key)) {
        nextActiveElement = children[event.key === HOME_KEY ? 0 : children.length - 1];
      } else {
        const isNext = [ARROW_RIGHT_KEY, ARROW_DOWN_KEY].includes(event.key);
        nextActiveElement = getNextActiveElement(children, event.target, isNext, true);
      }
      if (nextActiveElement) {
        nextActiveElement.focus({
          preventScroll: true
        });
        Tab.getOrCreateInstance(nextActiveElement).show();
      }
    }
    _getChildren() {
      // collection of inner elements
      return SelectorEngine.find(SELECTOR_INNER_ELEM, this._parent);
    }
    _getActiveElem() {
      return this._getChildren().find(child => this._elemIsActive(child)) || null;
    }
    _setInitialAttributes(parent, children) {
      this._setAttributeIfNotExists(parent, 'role', 'tablist');
      for (const child of children) {
        this._setInitialAttributesOnChild(child);
      }
    }
    _setInitialAttributesOnChild(child) {
      child = this._getInnerElement(child);
      const isActive = this._elemIsActive(child);
      const outerElem = this._getOuterElement(child);
      child.setAttribute('aria-selected', isActive);
      if (outerElem !== child) {
        this._setAttributeIfNotExists(outerElem, 'role', 'presentation');
      }
      if (!isActive) {
        child.setAttribute('tabindex', '-1');
      }
      this._setAttributeIfNotExists(child, 'role', 'tab');

      // set attributes to the related panel too
      this._setInitialAttributesOnTargetPanel(child);
    }
    _setInitialAttributesOnTargetPanel(child) {
      const target = SelectorEngine.getElementFromSelector(child);
      if (!target) {
        return;
      }
      this._setAttributeIfNotExists(target, 'role', 'tabpanel');
      if (child.id) {
        this._setAttributeIfNotExists(target, 'aria-labelledby', `${child.id}`);
      }
    }
    _toggleDropDown(element, open) {
      const outerElem = this._getOuterElement(element);
      if (!outerElem.classList.contains(CLASS_DROPDOWN)) {
        return;
      }
      const toggle = (selector, className) => {
        const element = SelectorEngine.findOne(selector, outerElem);
        if (element) {
          element.classList.toggle(className, open);
        }
      };
      toggle(SELECTOR_DROPDOWN_TOGGLE, CLASS_NAME_ACTIVE);
      toggle(SELECTOR_DROPDOWN_MENU, CLASS_NAME_SHOW$1);
      outerElem.setAttribute('aria-expanded', open);
    }
    _setAttributeIfNotExists(element, attribute, value) {
      if (!element.hasAttribute(attribute)) {
        element.setAttribute(attribute, value);
      }
    }
    _elemIsActive(elem) {
      return elem.classList.contains(CLASS_NAME_ACTIVE);
    }

    // Try to get the inner element (usually the .nav-link)
    _getInnerElement(elem) {
      return elem.matches(SELECTOR_INNER_ELEM) ? elem : SelectorEngine.findOne(SELECTOR_INNER_ELEM, elem);
    }

    // Try to get the outer element (usually the .nav-item)
    _getOuterElement(elem) {
      return elem.closest(SELECTOR_OUTER) || elem;
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Tab.getOrCreateInstance(this);
        if (typeof config !== 'string') {
          return;
        }
        if (data[config] === undefined || config.startsWith('_') || config === 'constructor') {
          throw new TypeError(`No method named "${config}"`);
        }
        data[config]();
      });
    }
  }

  /**
   * Data API implementation
   */

  EventHandler.on(document, EVENT_CLICK_DATA_API, SELECTOR_DATA_TOGGLE, function (event) {
    if (['A', 'AREA'].includes(this.tagName)) {
      event.preventDefault();
    }
    if (isDisabled(this)) {
      return;
    }
    Tab.getOrCreateInstance(this).show();
  });

  /**
   * Initialize on focus
   */
  EventHandler.on(window, EVENT_LOAD_DATA_API, () => {
    for (const element of SelectorEngine.find(SELECTOR_DATA_TOGGLE_ACTIVE)) {
      Tab.getOrCreateInstance(element);
    }
  });
  /**
   * jQuery
   */

  defineJQueryPlugin(Tab);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap toast.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */


  /**
   * Constants
   */

  const NAME = 'toast';
  const DATA_KEY = 'bs.toast';
  const EVENT_KEY = `.${DATA_KEY}`;
  const EVENT_MOUSEOVER = `mouseover${EVENT_KEY}`;
  const EVENT_MOUSEOUT = `mouseout${EVENT_KEY}`;
  const EVENT_FOCUSIN = `focusin${EVENT_KEY}`;
  const EVENT_FOCUSOUT = `focusout${EVENT_KEY}`;
  const EVENT_HIDE = `hide${EVENT_KEY}`;
  const EVENT_HIDDEN = `hidden${EVENT_KEY}`;
  const EVENT_SHOW = `show${EVENT_KEY}`;
  const EVENT_SHOWN = `shown${EVENT_KEY}`;
  const CLASS_NAME_FADE = 'fade';
  const CLASS_NAME_HIDE = 'hide'; // @deprecated - kept here only for backwards compatibility
  const CLASS_NAME_SHOW = 'show';
  const CLASS_NAME_SHOWING = 'showing';
  const DefaultType = {
    animation: 'boolean',
    autohide: 'boolean',
    delay: 'number'
  };
  const Default = {
    animation: true,
    autohide: true,
    delay: 5000
  };

  /**
   * Class definition
   */

  class Toast extends BaseComponent {
    constructor(element, config) {
      super(element, config);
      this._timeout = null;
      this._hasMouseInteraction = false;
      this._hasKeyboardInteraction = false;
      this._setListeners();
    }

    // Getters
    static get Default() {
      return Default;
    }
    static get DefaultType() {
      return DefaultType;
    }
    static get NAME() {
      return NAME;
    }

    // Public
    show() {
      const showEvent = EventHandler.trigger(this._element, EVENT_SHOW);
      if (showEvent.defaultPrevented) {
        return;
      }
      this._clearTimeout();
      if (this._config.animation) {
        this._element.classList.add(CLASS_NAME_FADE);
      }
      const complete = () => {
        this._element.classList.remove(CLASS_NAME_SHOWING);
        EventHandler.trigger(this._element, EVENT_SHOWN);
        this._maybeScheduleHide();
      };
      this._element.classList.remove(CLASS_NAME_HIDE); // @deprecated
      reflow(this._element);
      this._element.classList.add(CLASS_NAME_SHOW, CLASS_NAME_SHOWING);
      this._queueCallback(complete, this._element, this._config.animation);
    }
    hide() {
      if (!this.isShown()) {
        return;
      }
      const hideEvent = EventHandler.trigger(this._element, EVENT_HIDE);
      if (hideEvent.defaultPrevented) {
        return;
      }
      const complete = () => {
        this._element.classList.add(CLASS_NAME_HIDE); // @deprecated
        this._element.classList.remove(CLASS_NAME_SHOWING, CLASS_NAME_SHOW);
        EventHandler.trigger(this._element, EVENT_HIDDEN);
      };
      this._element.classList.add(CLASS_NAME_SHOWING);
      this._queueCallback(complete, this._element, this._config.animation);
    }
    dispose() {
      this._clearTimeout();
      if (this.isShown()) {
        this._element.classList.remove(CLASS_NAME_SHOW);
      }
      super.dispose();
    }
    isShown() {
      return this._element.classList.contains(CLASS_NAME_SHOW);
    }

    // Private

    _maybeScheduleHide() {
      if (!this._config.autohide) {
        return;
      }
      if (this._hasMouseInteraction || this._hasKeyboardInteraction) {
        return;
      }
      this._timeout = setTimeout(() => {
        this.hide();
      }, this._config.delay);
    }
    _onInteraction(event, isInteracting) {
      switch (event.type) {
        case 'mouseover':
        case 'mouseout':
          {
            this._hasMouseInteraction = isInteracting;
            break;
          }
        case 'focusin':
        case 'focusout':
          {
            this._hasKeyboardInteraction = isInteracting;
            break;
          }
      }
      if (isInteracting) {
        this._clearTimeout();
        return;
      }
      const nextElement = event.relatedTarget;
      if (this._element === nextElement || this._element.contains(nextElement)) {
        return;
      }
      this._maybeScheduleHide();
    }
    _setListeners() {
      EventHandler.on(this._element, EVENT_MOUSEOVER, event => this._onInteraction(event, true));
      EventHandler.on(this._element, EVENT_MOUSEOUT, event => this._onInteraction(event, false));
      EventHandler.on(this._element, EVENT_FOCUSIN, event => this._onInteraction(event, true));
      EventHandler.on(this._element, EVENT_FOCUSOUT, event => this._onInteraction(event, false));
    }
    _clearTimeout() {
      clearTimeout(this._timeout);
      this._timeout = null;
    }

    // Static
    static jQueryInterface(config) {
      return this.each(function () {
        const data = Toast.getOrCreateInstance(this, config);
        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config](this);
        }
      });
    }
  }

  /**
   * Data API implementation
   */

  enableDismissTrigger(Toast);

  /**
   * jQuery
   */

  defineJQueryPlugin(Toast);

  /**
   * --------------------------------------------------------------------------
   * Bootstrap index.umd.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/main/LICENSE)
   * --------------------------------------------------------------------------
   */

  const index_umd = {
    Alert,
    Button,
    Carousel,
    Collapse,
    Dropdown,
    Modal,
    Offcanvas,
    Popover,
    ScrollSpy,
    Tab,
    Toast,
    Tooltip
  };

  return index_umd;

}));
//# sourceMappingURL=bootstrap.bundle.js.map

;
/**!
 * FlexSearch.js v0.7.41 (Bundle)
 * Author and Copyright: Thomas Wilkerling
 * Licence: Apache-2.0
 * Hosted by Nextapps GmbH
 * https://github.com/nextapps-de/flexsearch
 */
(function _f(self){'use strict';try{if(module)self=module}catch(e){}self._factory=_f;var t;function u(a){return"undefined"!==typeof a?a:!0}function v(a){const b=Array(a);for(let c=0;c<a;c++)b[c]=x();return b}function x(){return Object.create(null)}function aa(a,b){return b.length-a.length}function C(a){return"string"===typeof a}function D(a){return"object"===typeof a}function E(a){return"function"===typeof a};function ba(a,b){var c=ca;if(a&&(b&&(a=F(a,b)),this.H&&(a=F(a,this.H)),this.J&&1<a.length&&(a=F(a,this.J)),c||""===c)){b=a.split(c);if(this.filter){a=this.filter;c=b.length;const d=[];for(let e=0,f=0;e<c;e++){const h=b[e];h&&!a[h]&&(d[f++]=h)}a=d}else a=b;return a}return a}const ca=/[\p{Z}\p{S}\p{P}\p{C}]+/u,da=/[\u0300-\u036f]/g;
function ea(a,b){const c=Object.keys(a),d=c.length,e=[];let f="",h=0;for(let g=0,k,m;g<d;g++)k=c[g],(m=a[k])?(e[h++]=G(b?"(?!\\b)"+k+"(\\b|_)":k),e[h++]=m):f+=(f?"|":"")+k;f&&(e[h++]=G(b?"(?!\\b)("+f+")(\\b|_)":"("+f+")"),e[h]="");return e}function F(a,b){for(let c=0,d=b.length;c<d&&(a=a.replace(b[c],b[c+1]),a);c+=2);return a}function G(a){return new RegExp(a,"g")}function fa(a){let b="",c="";for(let d=0,e=a.length,f;d<e;d++)(f=a[d])!==c&&(b+=c=f);return b};var ia={encode:ha,F:!1,G:""};function ha(a){return ba.call(this,(""+a).toLowerCase(),!1)};const ja={},I={};function ka(a){J(a,"add");J(a,"append");J(a,"search");J(a,"update");J(a,"remove")}function J(a,b){a[b+"Async"]=function(){const c=this,d=arguments;var e=d[d.length-1];let f;E(e)&&(f=e,delete d[d.length-1]);e=new Promise(function(h){setTimeout(function(){c.async=!0;const g=c[b].apply(c,d);c.async=!1;h(g)})});return f?(e.then(f),this):e}};function la(a,b,c,d){const e=a.length;let f=[],h,g,k=0;d&&(d=[]);for(let m=e-1;0<=m;m--){const n=a[m],w=n.length,q=x();let r=!h;for(let l=0;l<w;l++){const p=n[l],A=p.length;if(A)for(let B=0,z,y;B<A;B++)if(y=p[B],h){if(h[y]){if(!m)if(c)c--;else if(f[k++]=y,k===b)return f;if(m||d)q[y]=1;r=!0}if(d&&(z=(g[y]||0)+1,g[y]=z,z<e)){const H=d[z-2]||(d[z-2]=[]);H[H.length]=y}}else q[y]=1}if(d)h||(g=q);else if(!r)return[];h=q}if(d)for(let m=d.length-1,n,w;0<=m;m--){n=d[m];w=n.length;for(let q=0,r;q<w;q++)if(r=
n[q],!h[r]){if(c)c--;else if(f[k++]=r,k===b)return f;h[r]=1}}return f}function ma(a,b){const c=x(),d=x(),e=[];for(let f=0;f<a.length;f++)c[a[f]]=1;for(let f=0,h;f<b.length;f++){h=b[f];for(let g=0,k;g<h.length;g++)k=h[g],c[k]&&!d[k]&&(d[k]=1,e[e.length]=k)}return e};function K(a){this.l=!0!==a&&a;this.cache=x();this.h=[]}function na(a,b,c){D(a)&&(a=a.query);let d=this.cache.get(a);d||(d=this.search(a,b,c),this.cache.set(a,d));return d}K.prototype.set=function(a,b){if(!this.cache[a]){var c=this.h.length;c===this.l?delete this.cache[this.h[c-1]]:c++;for(--c;0<c;c--)this.h[c]=this.h[c-1];this.h[0]=a}this.cache[a]=b};K.prototype.get=function(a){const b=this.cache[a];if(this.l&&b&&(a=this.h.indexOf(a))){const c=this.h[a-1];this.h[a-1]=this.h[a];this.h[a]=c}return b};const pa={memory:{charset:"latin:extra",D:3,B:4,m:!1},performance:{D:3,B:3,s:!1,context:{depth:2,D:1}},match:{charset:"latin:extra",G:"reverse"},score:{charset:"latin:advanced",D:20,B:3,context:{depth:3,D:9}},"default":{}};function qa(a,b,c,d,e,f,h,g){setTimeout(function(){const k=a(c?c+"."+d:d,JSON.stringify(h));k&&k.then?k.then(function(){b.export(a,b,c,e,f+1,g)}):b.export(a,b,c,e,f+1,g)})};function L(a,b){if(!(this instanceof L))return new L(a);var c;if(a){C(a)?a=pa[a]:(c=a.preset)&&(a=Object.assign({},c[c],a));c=a.charset;var d=a.lang;C(c)&&(-1===c.indexOf(":")&&(c+=":default"),c=I[c]);C(d)&&(d=ja[d])}else a={};let e,f,h=a.context||{};this.encode=a.encode||c&&c.encode||ha;this.register=b||x();this.D=e=a.resolution||9;this.G=b=c&&c.G||a.tokenize||"strict";this.depth="strict"===b&&h.depth;this.l=u(h.bidirectional);this.s=f=u(a.optimize);this.m=u(a.fastupdate);this.B=a.minlength||1;this.C=
a.boost;this.map=f?v(e):x();this.A=e=h.resolution||1;this.h=f?v(e):x();this.F=c&&c.F||a.rtl;this.H=(b=a.matcher||d&&d.H)&&ea(b,!1);this.J=(b=a.stemmer||d&&d.J)&&ea(b,!0);if(c=b=a.filter||d&&d.filter){c=b;d=x();for(let g=0,k=c.length;g<k;g++)d[c[g]]=1;c=d}this.filter=c;this.cache=(b=a.cache)&&new K(b)}t=L.prototype;t.append=function(a,b){return this.add(a,b,!0)};
t.add=function(a,b,c,d){if(b&&(a||0===a)){if(!d&&!c&&this.register[a])return this.update(a,b);b=this.encode(b);if(d=b.length){const m=x(),n=x(),w=this.depth,q=this.D;for(let r=0;r<d;r++){let l=b[this.F?d-1-r:r];var e=l.length;if(l&&e>=this.B&&(w||!n[l])){var f=M(q,d,r),h="";switch(this.G){case "full":if(2<e){for(f=0;f<e;f++)for(var g=e;g>f;g--)if(g-f>=this.B){var k=M(q,d,r,e,f);h=l.substring(f,g);N(this,n,h,k,a,c)}break}case "reverse":if(1<e){for(g=e-1;0<g;g--)h=l[g]+h,h.length>=this.B&&N(this,n,
h,M(q,d,r,e,g),a,c);h=""}case "forward":if(1<e){for(g=0;g<e;g++)h+=l[g],h.length>=this.B&&N(this,n,h,f,a,c);break}default:if(this.C&&(f=Math.min(f/this.C(b,l,r)|0,q-1)),N(this,n,l,f,a,c),w&&1<d&&r<d-1)for(e=x(),h=this.A,f=l,g=Math.min(w+1,d-r),e[f]=1,k=1;k<g;k++)if((l=b[this.F?d-1-r-k:r+k])&&l.length>=this.B&&!e[l]){e[l]=1;const p=this.l&&l>f;N(this,m,p?f:l,M(h+(d/2>h?0:1),d,r,g-1,k-1),a,c,p?l:f)}}}}this.m||(this.register[a]=1)}}return this};
function M(a,b,c,d,e){return c&&1<a?b+(d||0)<=a?c+(e||0):(a-1)/(b+(d||0))*(c+(e||0))+1|0:0}function N(a,b,c,d,e,f,h){let g=h?a.h:a.map;if(!b[c]||h&&!b[c][h])a.s&&(g=g[d]),h?(b=b[c]||(b[c]=x()),b[h]=1,g=g[h]||(g[h]=x())):b[c]=1,g=g[c]||(g[c]=[]),a.s||(g=g[d]||(g[d]=[])),f&&g.includes(e)||(g[g.length]=e,a.m&&(a=a.register[e]||(a.register[e]=[]),a[a.length]=g))}
t.search=function(a,b,c){c||(!b&&D(a)?(c=a,a=c.query):D(b)&&(c=b));let d=[],e;let f,h=0;if(c){a=c.query||a;b=c.limit;h=c.offset||0;var g=c.context;f=c.suggest}if(a&&(a=this.encode(""+a),e=a.length,1<e)){c=x();var k=[];for(let n=0,w=0,q;n<e;n++)if((q=a[n])&&q.length>=this.B&&!c[q])if(this.s||f||this.map[q])k[w++]=q,c[q]=1;else return d;a=k;e=a.length}if(!e)return d;b||(b=100);g=this.depth&&1<e&&!1!==g;c=0;let m;g?(m=a[0],c=1):1<e&&a.sort(aa);for(let n,w;c<e;c++){w=a[c];g?(n=ra(this,d,f,b,h,2===e,w,
m),f&&!1===n&&d.length||(m=w)):n=ra(this,d,f,b,h,1===e,w);if(n)return n;if(f&&c===e-1){k=d.length;if(!k){if(g){g=0;c=-1;continue}return d}if(1===k)return sa(d[0],b,h)}}return la(d,b,h,f)};
function ra(a,b,c,d,e,f,h,g){let k=[],m=g?a.h:a.map;a.s||(m=ta(m,h,g,a.l));if(m){let n=0;const w=Math.min(m.length,g?a.A:a.D);for(let q=0,r=0,l,p;q<w;q++)if(l=m[q])if(a.s&&(l=ta(l,h,g,a.l)),e&&l&&f&&(p=l.length,p<=e?(e-=p,l=null):(l=l.slice(e),e=0)),l&&(k[n++]=l,f&&(r+=l.length,r>=d)))break;if(n){if(f)return sa(k,d,0);b[b.length]=k;return}}return!c&&k}function sa(a,b,c){a=1===a.length?a[0]:[].concat.apply([],a);return c||a.length>b?a.slice(c,c+b):a}
function ta(a,b,c,d){c?(d=d&&b>c,a=(a=a[d?b:c])&&a[d?c:b]):a=a[b];return a}t.contain=function(a){return!!this.register[a]};t.update=function(a,b){return this.remove(a).add(a,b)};
t.remove=function(a,b){const c=this.register[a];if(c){if(this.m)for(let d=0,e;d<c.length;d++)e=c[d],e.splice(e.indexOf(a),1);else O(this.map,a,this.D,this.s),this.depth&&O(this.h,a,this.A,this.s);b||delete this.register[a];if(this.cache){b=this.cache;for(let d=0,e,f;d<b.h.length;d++)f=b.h[d],e=b.cache[f],e.includes(a)&&(b.h.splice(d--,1),delete b.cache[f])}}return this};
function O(a,b,c,d,e){let f=0;if(a.constructor===Array)if(e)b=a.indexOf(b),-1!==b?1<a.length&&(a.splice(b,1),f++):f++;else{e=Math.min(a.length,c);for(let h=0,g;h<e;h++)if(g=a[h])f=O(g,b,c,d,e),d||f||delete a[h]}else for(let h in a)(f=O(a[h],b,c,d,e))||delete a[h];return f}t.searchCache=na;
t.export=function(a,b,c,d,e,f){let h=!0;"undefined"===typeof f&&(h=new Promise(m=>{f=m}));let g,k;switch(e||(e=0)){case 0:g="reg";if(this.m){k=x();for(let m in this.register)k[m]=1}else k=this.register;break;case 1:g="cfg";k={doc:0,opt:this.s?1:0};break;case 2:g="map";k=this.map;break;case 3:g="ctx";k=this.h;break;default:"undefined"===typeof c&&f&&f();return}qa(a,b||this,c,g,d,e,k,f);return h};
t.import=function(a,b){if(b)switch(C(b)&&(b=JSON.parse(b)),a){case "cfg":this.s=!!b.opt;break;case "reg":this.m=!1;this.register=b;break;case "map":this.map=b;break;case "ctx":this.h=b}};ka(L.prototype);function ua(a){a=a.data;var b=self._index;const c=a.args;var d=a.task;switch(d){case "init":d=a.options||{};a=a.factory;b=d.encode;d.cache=!1;b&&0===b.indexOf("function")&&(d.encode=Function("return "+b)());a?(Function("return "+a)()(self),self._index=new self.FlexSearch.Index(d),delete self.FlexSearch):self._index=new L(d);break;default:a=a.id,b=b[d].apply(b,c),postMessage("search"===d?{id:a,msg:b}:{id:a})}};let va=0;function P(a){if(!(this instanceof P))return new P(a);var b;a?E(b=a.encode)&&(a.encode=b.toString()):a={};(b=(self||window)._factory)&&(b=b.toString());const c="undefined"===typeof window&&self.exports,d=this;this.o=wa(b,c,a.worker);this.h=x();if(this.o){if(c)this.o.on("message",function(e){d.h[e.id](e.msg);delete d.h[e.id]});else this.o.onmessage=function(e){e=e.data;d.h[e.id](e.msg);delete d.h[e.id]};this.o.postMessage({task:"init",factory:b,options:a})}}Q("add");Q("append");Q("search");
Q("update");Q("remove");function Q(a){P.prototype[a]=P.prototype[a+"Async"]=function(){const b=this,c=[].slice.call(arguments);var d=c[c.length-1];let e;E(d)&&(e=d,c.splice(c.length-1,1));d=new Promise(function(f){setTimeout(function(){b.h[++va]=f;b.o.postMessage({task:a,id:va,args:c})})});return e?(d.then(e),this):d}}
function wa(a,b,c){let d;try{d=b?new (require("worker_threads")["Worker"])(__dirname + "/node/node.js"):a?new Worker(URL.createObjectURL(new Blob(["onmessage="+ua.toString()],{type:"text/javascript"}))):new Worker(C(c)?c:"worker/worker.js",{type:"module"})}catch(e){}return d};function S(a){if(!(this instanceof S))return new S(a);var b=a.document||a.doc||a,c;this.K=[];this.h=[];this.A=[];this.register=x();this.key=(c=b.key||b.id)&&T(c,this.A)||"id";this.m=u(a.fastupdate);this.C=(c=b.store)&&!0!==c&&[];this.store=c&&x();this.I=(c=b.tag)&&T(c,this.A);this.l=c&&x();this.cache=(c=a.cache)&&new K(c);a.cache=!1;this.o=a.worker;this.async=!1;c=x();let d=b.index||b.field||b;C(d)&&(d=[d]);for(let e=0,f,h;e<d.length;e++)f=d[e],C(f)||(h=f,f=f.field),h=D(h)?Object.assign({},a,h):a,
this.o&&(c[f]=new P(h),c[f].o||(this.o=!1)),this.o||(c[f]=new L(h,this.register)),this.K[e]=T(f,this.A),this.h[e]=f;if(this.C)for(a=b.store,C(a)&&(a=[a]),b=0;b<a.length;b++)this.C[b]=T(a[b],this.A);this.index=c}function T(a,b){const c=a.split(":");let d=0;for(let e=0;e<c.length;e++)a=c[e],0<=a.indexOf("[]")&&(a=a.substring(0,a.length-2))&&(b[d]=!0),a&&(c[d++]=a);d<c.length&&(c.length=d);return 1<d?c:c[0]}function U(a,b){if(C(b))a=a[b];else for(let c=0;a&&c<b.length;c++)a=a[b[c]];return a}
function V(a,b,c,d,e){a=a[e];if(d===c.length-1)b[e]=a;else if(a)if(a.constructor===Array)for(b=b[e]=Array(a.length),e=0;e<a.length;e++)V(a,b,c,d,e);else b=b[e]||(b[e]=x()),e=c[++d],V(a,b,c,d,e)}function X(a,b,c,d,e,f,h,g){if(a=a[h])if(d===b.length-1){if(a.constructor===Array){if(c[d]){for(b=0;b<a.length;b++)e.add(f,a[b],!0,!0);return}a=a.join(" ")}e.add(f,a,g,!0)}else if(a.constructor===Array)for(h=0;h<a.length;h++)X(a,b,c,d,e,f,h,g);else h=b[++d],X(a,b,c,d,e,f,h,g)}t=S.prototype;
t.add=function(a,b,c){D(a)&&(b=a,a=U(b,this.key));if(b&&(a||0===a)){if(!c&&this.register[a])return this.update(a,b);for(let d=0,e,f;d<this.h.length;d++)f=this.h[d],e=this.K[d],C(e)&&(e=[e]),X(b,e,this.A,0,this.index[f],a,e[0],c);if(this.I){let d=U(b,this.I),e=x();C(d)&&(d=[d]);for(let f=0,h,g;f<d.length;f++)if(h=d[f],!e[h]&&(e[h]=1,g=this.l[h]||(this.l[h]=[]),!c||!g.includes(a)))if(g[g.length]=a,this.m){const k=this.register[a]||(this.register[a]=[]);k[k.length]=g}}if(this.store&&(!c||!this.store[a])){let d;
if(this.C){d=x();for(let e=0,f;e<this.C.length;e++)f=this.C[e],C(f)?d[f]=b[f]:V(b,d,f,0,f[0])}this.store[a]=d||b}}return this};t.append=function(a,b){return this.add(a,b,!0)};t.update=function(a,b){return this.remove(a).add(a,b)};
t.remove=function(a){D(a)&&(a=U(a,this.key));if(this.register[a]){for(var b=0;b<this.h.length&&(this.index[this.h[b]].remove(a,!this.o),!this.m);b++);if(this.I&&!this.m)for(let c in this.l){b=this.l[c];const d=b.indexOf(a);-1!==d&&(1<b.length?b.splice(d,1):delete this.l[c])}this.store&&delete this.store[a];delete this.register[a]}return this};
t.search=function(a,b,c,d){c||(!b&&D(a)?(c=a,a=""):D(b)&&(c=b,b=0));let e=[],f=[],h,g,k,m,n,w,q=0;if(c)if(c.constructor===Array)k=c,c=null;else{a=c.query||a;k=(h=c.pluck)||c.index||c.field;m=c.tag;g=this.store&&c.enrich;n="and"===c.bool;b=c.limit||b||100;w=c.offset||0;if(m&&(C(m)&&(m=[m]),!a)){for(let l=0,p;l<m.length;l++)if(p=xa.call(this,m[l],b,w,g))e[e.length]=p,q++;return q?e:[]}C(k)&&(k=[k])}k||(k=this.h);n=n&&(1<k.length||m&&1<m.length);const r=!d&&(this.o||this.async)&&[];for(let l=0,p,A,B;l<
k.length;l++){let z;A=k[l];C(A)||(z=A,A=z.field,a=z.query||a,b=z.limit||b,g=z.enrich||g);if(r)r[l]=this.index[A].searchAsync(a,b,z||c);else{d?p=d[l]:p=this.index[A].search(a,b,z||c);B=p&&p.length;if(m&&B){const y=[];let H=0;n&&(y[0]=[p]);for(let W=0,oa,R;W<m.length;W++)if(oa=m[W],B=(R=this.l[oa])&&R.length)H++,y[y.length]=n?[R]:R;H&&(p=n?la(y,b||100,w||0):ma(p,y),B=p.length)}if(B)f[q]=A,e[q++]=p;else if(n)return[]}}if(r){const l=this;return new Promise(function(p){Promise.all(r).then(function(A){p(l.search(a,
b,c,A))})})}if(!q)return[];if(h&&(!g||!this.store))return e[0];for(let l=0,p;l<f.length;l++){p=e[l];p.length&&g&&(p=ya.call(this,p));if(h)return p;e[l]={field:f[l],result:p}}return e};function xa(a,b,c,d){let e=this.l[a],f=e&&e.length-c;if(f&&0<f){if(f>b||c)e=e.slice(c,c+b);d&&(e=ya.call(this,e));return{tag:a,result:e}}}function ya(a){const b=Array(a.length);for(let c=0,d;c<a.length;c++)d=a[c],b[c]={id:d,doc:this.store[d]};return b}t.contain=function(a){return!!this.register[a]};t.get=function(a){return this.store[a]};
t.set=function(a,b){this.store[a]=b;return this};t.searchCache=na;t.export=function(a,b,c,d,e,f){let h;"undefined"===typeof f&&(h=new Promise(g=>{f=g}));e||(e=0);d||(d=0);if(d<this.h.length){const g=this.h[d],k=this.index[g];b=this;setTimeout(function(){k.export(a,b,e?g:"",d,e++,f)||(d++,e=1,b.export(a,b,g,d,e,f))})}else{let g,k;switch(e){case 1:g="tag";k=this.l;c=null;break;case 2:g="store";k=this.store;c=null;break;default:f();return}qa(a,this,c,g,d,e,k,f)}return h};
t.import=function(a,b){if(b)switch(C(b)&&(b=JSON.parse(b)),a){case "tag":this.l=b;break;case "reg":this.m=!1;this.register=b;for(let d=0,e;d<this.h.length;d++)e=this.index[this.h[d]],e.register=b,e.m=!1;break;case "store":this.store=b;break;default:a=a.split(".");const c=a[0];a=a[1];c&&a&&this.index[c].import(a,b)}};ka(S.prototype);var Aa={encode:za,F:!1,G:""};const Ba=[G("[\u00e0\u00e1\u00e2\u00e3\u00e4\u00e5]"),"a",G("[\u00e8\u00e9\u00ea\u00eb]"),"e",G("[\u00ec\u00ed\u00ee\u00ef]"),"i",G("[\u00f2\u00f3\u00f4\u00f5\u00f6\u0151]"),"o",G("[\u00f9\u00fa\u00fb\u00fc\u0171]"),"u",G("[\u00fd\u0177\u00ff]"),"y",G("\u00f1"),"n",G("[\u00e7c]"),"k",G("\u00df"),"s",G(" & ")," and "];function za(a){var b=a=""+a;b.normalize&&(b=b.normalize("NFD").replace(da,""));return ba.call(this,b.toLowerCase(),!a.normalize&&Ba)};var Da={encode:Ca,F:!1,G:"strict"};const Ea=/[^a-z0-9]+/,Fa={b:"p",v:"f",w:"f",z:"s",x:"s","\u00df":"s",d:"t",n:"m",c:"k",g:"k",j:"k",q:"k",i:"e",y:"e",u:"o"};function Ca(a){a=za.call(this,a).join(" ");const b=[];if(a){const c=a.split(Ea),d=c.length;for(let e=0,f,h=0;e<d;e++)if((a=c[e])&&(!this.filter||!this.filter[a])){f=a[0];let g=Fa[f]||f,k=g;for(let m=1;m<a.length;m++){f=a[m];const n=Fa[f]||f;n&&n!==k&&(g+=n,k=n)}b[h++]=g}}return b};var Ha={encode:Ga,F:!1,G:""};const Ia=[G("ae"),"a",G("oe"),"o",G("sh"),"s",G("th"),"t",G("ph"),"f",G("pf"),"f",G("(?![aeo])h(?![aeo])"),"",G("(?!^[aeo])h(?!^[aeo])"),""];function Ga(a,b){a&&(a=Ca.call(this,a).join(" "),2<a.length&&(a=F(a,Ia)),b||(1<a.length&&(a=fa(a)),a&&(a=a.split(" "))));return a||[]};var Ka={encode:Ja,F:!1,G:""};const La=G("(?!\\b)[aeo]");function Ja(a){a&&(a=Ga.call(this,a,!0),1<a.length&&(a=a.replace(La,"")),1<a.length&&(a=fa(a)),a&&(a=a.split(" ")));return a||[]};I["latin:default"]=ia;I["latin:simple"]=Aa;I["latin:balance"]=Da;I["latin:advanced"]=Ha;I["latin:extra"]=Ka;const Y={Index:L,Document:S,Worker:P,registerCharset:function(a,b){I[a]=b},registerLanguage:function(a,b){ja[a]=b}};let Z;(Z=self.define)&&Z.amd?Z([],function(){return Y}):self.exports?self.exports=Y:self.FlexSearch=Y;}(this));

;
const search = document.querySelector('.search-input')
const suggestions = document.querySelector('.search-suggestions')
const background = document.querySelector('.search-background')

var index = new FlexSearch.Document({
  tokenize: "forward",
  cache: 100,
  document: {
    id: "id",
    tag: "tag",
    store: ["href", "title", "description"],
    index: ["title", "description", "content"]
  }
});

/*
Source:
  - https://github.com/nextapps-de/flexsearch#index-documents-field-search
  - https://raw.githack.com/nextapps-de/flexsearch/master/demo/autocomplete.html
*/
function initIndex() {
  // https://discourse.gohugo.io/t/range-length-or-last-element/3803/2
  // Note: pages without a title (such as browserconfig.xml) are excluded
  
  
  
  index.add(
    
      
      {
        id: 0,
        tag: "en",
        href: "/docs/library/abbr/",
        title: "Abbr",
        description: "Use the abbr shortcode to show the long form of an abbrevitation.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 1,
        tag: "en",
        href: "/docs/library/alert/",
        title: "Alert",
        description: "Use the alert shortcode to display a contextual feedback message.",
        
        
        content: "Alert \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 2,
        tag: "en",
        href: "/docs/library/animation/",
        title: "Animation",
        description: "Use the animation shortcode to show an After Effects animation.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 3,
        tag: "en",
        href: "/docs/library/args/",
        title: "Args",
        description: "Use the args shortcode to generates a table of structured arguments.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 4,
        tag: "en",
        href: "/docs/library/badge/",
        title: "Badge",
        description: "Use the badge shortcode to enrich headings.",
        
        
        content: "Badge \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 5,
        tag: "en",
        href: "/examples/cable-stayed/",
        title: "Cable Stayed",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 6,
        tag: "en",
        href: "/docs/library/card/",
        title: "Card",
        description: "Use the card shortcode to display a card that links to a content page.",
        
        
        content: "Card \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 7,
        tag: "en",
        href: "/docs/library/card-group/",
        title: "Card Group",
        description: "Use the card-group shortcode to display a group of cards.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 8,
        tag: "en",
        href: "/docs/configuration/colors/",
        title: "Colors",
        description: "Use Bootstrap's color system to easily adjust your website's colors.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 9,
        tag: "en",
        href: "/docs/getting-started/command-line/",
        title: "Command line",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 10,
        tag: "en",
        href: "/docs/library/command-prompt/",
        title: "Command Prompt",
        description: "The command shortcode generates terminal output for either Bash, PowerShell, or SQL shell languages.",
        
        
        content: "Overview \u0026nbsp; Added in v0.5.0\u0026nbsp; \u0026nbsp; The command shortcode generates terminal output for either bash, powershell, or sql shell languages. The following example generates a block with a default bash command prompt.\nexport MY_VAR=123 markdown \u0026lt; command \u0026gt; export MY_VAR=123 \u0026lt; /command \u0026gt; Arguments \u0026nbsp; The shortcode supports the following arguments:\nName Type Required Default Comment class string Class attribute of the command element. host string Host to add to the prompt, e.g. localhost. prompt string Prompt override, e.g. PS C:\\Users\\User\u0026gt;. shell select bash Type of shell. Supported values: [bash, powershell, sql]. user string User to add to the prompt, e.g. user. Examples \u0026nbsp; Change the style and language of your command prompt with shortcode arguments.\nBash \u0026nbsp; Specify user and host to add the user context to the prompt. In addition, use (out) to specify an output line and use \\ to denote a line continuation.\nexport MY_VAR=123 echo \u0026#34;hello\u0026#34; hello echo one \\ two \\ three one two three echo \u0026#34;goodbye\u0026#34; goodbye markdown \u0026lt; command user=\u0026#34;user\u0026#34; host=\u0026#34;localhost\u0026#34; \u0026gt; export MY_VAR=123 echo \u0026#34;hello\u0026#34; (out)hello echo one \\ two \\ three (out)one two three echo \u0026#34;goodbye\u0026#34; (out)goodbye \u0026lt; /command \u0026gt; PowerShell \u0026nbsp; Set the shell argument to powershell to generate a PowerShell terminal. Override the prompt to add a directory if needed. Use the backtick ` symbol to denote a line continuation.\nWrite-Host ` \u0026#39;Hello\u0026#39; ` \u0026#39;from\u0026#39; ` \u0026#39;PowerShell!\u0026#39; Hello from PowerShell! Write-Host \u0026#39;Goodbye from PowerShell!\u0026#39; Goodbye from PowerShell! markdown \u0026lt; command prompt=\u0026#34;PS C:\\Users\\User\u0026gt;\u0026#34; shell=\u0026#34;powershell\u0026#34; \u0026gt; Write-Host ` \u0026#39;Hello\u0026#39; ` \u0026#39;from\u0026#39; ` \u0026#39;PowerShell!\u0026#39; (out)Hello from PowerShell! Write-Host \u0026#39;Goodbye from PowerShell!\u0026#39; (out)Goodbye from PowerShell! \u0026lt; /command \u0026gt; SQL \u0026nbsp; Set the shell argument to sql to generate a SQL terminal. Use the (con) suffix to denote a line continuation.\nset @my_var = \u0026#39;foo\u0026#39;; set @my_other_var = \u0026#39;bar\u0026#39;; CREATE TABLE people ( first_name VARCHAR(30) NOT NULL, last_name VARCHAR(30) NOT NULL ); Query OK, 0 rows affected (0.09 sec) insert into people values (\u0026#39;John\u0026#39;, \u0026#39;Doe\u0026#39;); Query OK, 1 row affected (0.02 sec) select * from people order by last_name; +------------+-----------+ | first_name | last_name | +------------+-----------+ | John | Doe | +------------+-----------+ 1 row in set (0.00 sec) markdown \u0026lt; command prompt=\u0026#34;mysql\u0026gt;\u0026#34; shell=\u0026#34;sql\u0026#34; \u0026gt; set @my_var = \u0026#39;foo\u0026#39;; set @my_other_var = \u0026#39;bar\u0026#39;; CREATE TABLE people ((con) first_name VARCHAR(30) NOT NULL,(con) last_name VARCHAR(30) NOT NULL(con) ); (out)Query OK, 0 rows affected (0.09 sec) insert into people(con) values (\u0026#39;John\u0026#39;, \u0026#39;Doe\u0026#39;); (out)Query OK, 1 row affected (0.02 sec) select *(con) from people(con) order by last_name; (out)+------------+-----------+ (out)| first_name | last_name | (out)+------------+-----------+ (out)| John | Doe | (out)+------------+-----------+ (out)1 row in set (0.00 sec) \u0026lt; /command \u0026gt;"
      })
      .add(
      
      
      {
        id: 11,
        tag: "en",
        href: "/docs/getting-started/compiling/",
        title: "Compiling",
        description: "Compiling your own version of OpenSees.",
        
        
        content: "Prerequisites \u0026nbsp; Compiling OpenSees requires the following software to be installed on your local machine:\nSoftware Hugo npm Remarks Git\u0026nbsp; recommended \u0026nbsp; Recommended for version control Hugo (extended)\u0026nbsp; \u0026nbsp; Embedded as npm binary Node.js\u0026nbsp; \u0026nbsp; The installation package includes npm Installation \u0026nbsp; The next steps describe the approach how to initialize a new Hinode site using either Hugo or npm.\nWindows installation notes \u0026nbsp; The installation for Windows requires PowerShell v7. Download it from the Microsoft Store as needed. Check your current version with the command $PSVersionTable. CMake npm Create a directory to hold build artifacts\nmkdir build Configure the system for your system\ncd build cmake .. Start a development server\ncmake --build . --target OpenSees -j8 Create a new repository\nGo to github.com\u0026nbsp; and login to GitHub as needed. Next, click the green button Use this template \u0026nbsp; to initialize a new repository based on the Hinode template.\nAlternatively, you can use the GitHub cli\u0026nbsp; to initialize the repository from the command line. Replace --private with --public if you wish to create a public repository instead.\ngh repo create my-hinode-site --private --template=\u0026#34;https://github.com/gethinode/template.git\u0026#34; Configure a local site\nAssuming your repository is owner/my-hinode-site, use the git command to clone the repository to your local machine.\ngit clone https://github.com/owner/my-hinode-site \u0026amp;\u0026amp; cd my-hinode-site Now install the npm packages and hugo modules.\nnpm install \u0026amp;\u0026amp; npm run mod:update Start the development server\nnpm run start Considerations \u0026nbsp; Before deciding on your hosting and deployment approach, review the following considerations.\nInclude npm in your build process\nHinode supports npm to automate the build process. Visit the Hinode introduction and commands overview for more details.\nConfigure the build timeout\nYou might encounter timeout errors when you generate a large site that contains many resources (such as images). Adjust the timeout in config/_default/hugo.toml as needed.\nconfig/_default/hugo.toml timeout = \u0026#34;180s\u0026#34; ... Consider using build automation\nMany popular Git providers provide the option to automate the build and deployment process ( abbr \u0026ldquo;CI/CD\u0026rdquo; \u0026gt;). You can trigger this process on each release to your main repository branch, or set up a preview during a Pull Request. The examples on this page assume you have a Git repository with GitHub.\nUnderstand the support for custom domain names\nMost hosting providers provide a subdomain, such as \u0026lt;username\u0026gt;.github.io, to access your website by default. Usually you have the ability to use a custom domain instead, although additional services and configuration might be needed.\nThe table below gives a brief overview of the features supported by a few selected hosting providers. The next paragraphs describe the build and deployment process for each provider in more detail.\nFeature Azure blob storage Netlify Automation Custom action \u0026nbsp; Custom domain name Requires Azure CDN \u0026nbsp; CDN / Edge network Requires Azure CDN \u0026nbsp; HTTP headers Requires Azure CDN \u0026nbsp; Feature Azure blob storage Azure Static Web App GitHub pages Netlify Automation Custom action \u0026lt; fas check \u0026gt; \u0026lt; fas check \u0026gt; \u0026lt; fas check \u0026gt; Custom domain name Requires Azure CDN \u0026lt; fas check \u0026gt; \u0026lt; fas check \u0026gt; \u0026lt; fas check \u0026gt; CDN / Edge network Requires Azure CDN \u0026lt; fas check \u0026gt; \u0026lt; fas check \u0026gt; \u0026lt; fas check \u0026gt; HTTP headers Requires Azure CDN \u0026lt; fas check \u0026gt; \u0026lt; fas check \u0026gt; Host on Netlify \u0026nbsp; Netlify can host your website with continuous deployment from your Git provider. The starter price plan is free for any public repository and provides\n\u0026nbsp; Note The starter plan requires your repository to be public. You will require a paid plan if your repository is set to private.\nPreparations \u0026nbsp; The repository root should include a file netlify.toml. If not, copy it from the Hinode main repository\u0026nbsp; . The configuration file contains the build settings that Netlify will pick up when connecting to your repository. The panel below shows the default build settings. The key command to observe is npm run build, which ensures the site is built properly.\n\u0026nbsp; Note The default configuration provides basic security headers. Please review the server configuration for more details about the Content Security Policy. The cache settings are explained in more detail in the Netlify blog\u0026nbsp; .\nnetlify.toml [build] publish = \u0026#34;exampleSite/public\u0026#34; command = \u0026#34;npm run build:example\u0026#34; [build.environment] DART_SASS_VERSION = \u0026#34;1.77.5\u0026#34; HUGO_VERSION = \u0026#34;0.131.0\u0026#34; HUGO_ENV = \u0026#34;production\u0026#34; HUGO_ENABLEGITINFO = \u0026#34;true\u0026#34; NODE_VERSION = \u0026#34;20.16.0\u0026#34; NPM_VERSION = \u0026#34;10.8.1\u0026#34; ... The same file also configures several optional plugins.\nnetlify.toml [[plugins]] package = \u0026#34;@gethinode/netlify-plugin-dartsass\u0026#34; [[plugins]] package = \u0026#34;netlify-plugin-hugo-cache-resources\u0026#34; [plugins.inputs] # Redirected in exampleSite/config/_default/hugo.toml # srcdir = \u0026#34;\u0026#34; # [[plugins]] # package = \u0026#34;@netlify/plugin-lighthouse\u0026#34; # [plugins.inputs] # output_path = \u0026#34;reports/lighthouse.html\u0026#34; ... Configure your site \u0026nbsp; Sign up for Netlify and configure your site in seven steps.\nStep 1. Sign up for Netlify Step 2. Sign in with your Git provider Step 3. Authenticate your sign in (2FA) Step 4. Add a new site Step 5. Connect to your Git provider Step 6. Import an existing project Step 7. Configure the build settings Previous Next Step 1. Sign up for Netlify Go to netlify.com\u0026nbsp; and click on the button Sign up. Select your preferred signup method next. This will likely be a hosted Git provider, although you also have the option to sign up with an email address. The next steps use GitHub, but other Git providers will follow a similar process. Step 2. Sign in with your Git provider Enter the credentials for your Git provider and click the button to sign in. Step 3. Authenticate your sign in (2FA) Assuming you have enabled two-factor authentication with your Git provider, authenticate the sign in next. This example uses the GitHub Mobile app. Step 4. Add a new site Click on the button Add new site to set up a new site with Netlify. Step 5. Connect to your Git provider Connect to your Git provider to import your existing Hinode repository. Step 6. Import an existing project Pick a repository from your Git provider. Ensure Netlify has access to the correct repository. Step 7. Configure the build settings Review the basic build settings. Netlify will use the settings provided in the preparations. Click on the button Deploy site to start the build and deployment process. Your site is now ready to be used. Click on the domain settings of your site within the Site overview page to provide a domain alias and to edit the site name as needed. The same section also allows the configuration of a custom domain. Be sure to review your server configuration if you encounter any rendering issues, such as broken links or garbled stylesheets."
      })
      .add(
      
      
      {
        id: 12,
        tag: "en",
        href: "/examples/example8/",
        title: "Continuum Cantilever",
        description: "Dynamic analysis of a cantilever beam, modeled with 8-node brick elements.",
        
        
        content: "In this example a simple problem in solid dynamics is considered. The structure is a cantilever beam modelled with three dimensional solid elements.\nExample8.tcl Example8.py For three dimensional analysis, a typical solid element is defined as a volume in three dimensional space. Each node of the analysis has three displacement degrees of freedom. Thus the model is defined with ndm = 3 and ndf = 3.\nFor this model, a mesh is generated using the \u0026ldquo;block3D\u0026rdquo; command. The number of nodes in the local x-direction of the block is nx, the number of nodes in the local y-direction of the block is ny and the number of nodes in the local z-direction of the block is nz. The block3D generation nodes 1,2,3,4,5,6,7,8 are prescribed to define the three dimensional domain of the beam, which is of size 2×2×102 \\times 2 \\times 10 .\nTwo possible brick elements can be used for the analysis. These may be created using the terms StdBrick or BbarBrick. An elastic isotropic material is used.\nFor initial gravity load analysis, a single load pattern with a linear time series and a single nodal loads is used.\nBoundary conditions are applied using the fixZ command. In this case, all the nodes whose zz -coordiate is 0.00.0 have the boundary condition 1,1,1, fully fixed.\nA solution algorithm of type Newton is used for the problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. Five static load steps are performed.\nSubsequent to the static analysis, the wipeAnalysis and remove loadPatern commands are used to remove the nodal loads and create a new analysis. The nodal displacements have not changed. However, with the external loads removed the structure is no longer in static equilibrium.\nThe integrator for the dynamic analysis if of type GeneralizedMidpoint with α=0.5\\alpha = 0.5 . This choice is uconditionally stable and energy conserving for linear problems. Additionally, this integrator conserves linear and angular momentum for both linear and non-linear problems. The dynamic analysis is performed using 100100 time increments with a time step Δt=2.0\\Delta t = 2.0 .\nThe deformed shape at the end of the analysis is rendered below:\nThe results consist of the file cantilever.out, which contains a line for every time step. Each line contains the time and the horizontal displacement at the upper right corner the beam. This is plotted in the figure below:\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 13,
        tag: "en",
        href: "/docs/getting-started/contribute/",
        title: "Contribute",
        description: "Contribute to the open-source development of OpenSees.",
        
        
        content: "OpenSees is fully open source and welcomes any contribution. To streamline the contribution process, please take a moment to review the guidelines outlined in this article.\nUsing the issue tracker \u0026nbsp; The issue tracker\u0026nbsp; on GitHub is the preferred channel for bug reports, feature requests and submitting pull requests.\nAsking for help \u0026nbsp; Use the GitHub Discussions\u0026nbsp; to ask for help from the OpenSees community\u0026nbsp; . The discussion forum also includes other topics, such as ideas\u0026nbsp; and showcases\u0026nbsp; . We strive for a safe, welcoming, and productive community. The community guidelines\u0026nbsp; provide more context about the expectations, moderation policy, and terms of service.\nBug reports \u0026nbsp; A bug is a demonstrable problem that is caused by the code in the repository. This may also include issues with the documentation or configuration files. Before filing a bug report, please consider the following guidelines:\nUse the GitHub issue search\u0026nbsp; — check if the issue has already been reported. Check if the issue has been fixed — try to reproduce it using the latest main in the repository\u0026nbsp; . Isolate the problem — ideally create a reduced test case. Use the provided template in the issue tracker\u0026nbsp; to capture the context, evidence and steps on how to reproduce the issue. Feature requests \u0026nbsp; Feature requests are welcome. Please use the provided template in the issue tracker\u0026nbsp; to capture the idea and context.\nPull requests \u0026nbsp; \u0026nbsp; Important By submitting a patch, you agree to allow the project owners to license your work under the terms of the BSD license\u0026nbsp; (if it includes code changes) and under the terms of the Creative Commons ( CC BY-NC 4.0)\u0026nbsp; license (if it includes documentation changes).\nPlease adhere to the coding guidelines used throughout the project (indentation, accurate comments, etc.) and any other requirements (such as test coverage).\nAdhering to the following process is the best way to get your work included in the project:\nFork the project, clone your fork, and configure the remotes:\ngit clone https://github.com/\u0026lt;your-username\u0026gt;/OpenSeesRT.git cd OpenSeesRT git remote add upstream https://github.com/claudioperez/OpenSeesRT If you cloned a while ago, get the latest changes from upstream:\ngit checkout main git pull upstream main Create a new topic branch (off the main project development branch) to contain your feature, change, or fix:\ngit checkout -b \u0026lt;topic-branch-name\u0026gt; Commit your changes in logical chunks. Please adhere to these git commit message guidelines\u0026nbsp; . Use Git\u0026rsquo;s interactive rebase\u0026nbsp; feature to tidy up your commits before making them public.\nLocally merge (or rebase) the upstream development branch into your topic branch:\ngit pull [--rebase] upstream main Push your topic branch up to your fork:\ngit push origin \u0026lt;topic-branch-name\u0026gt; Open a Pull Request\u0026nbsp; with a clear title and description against the main branch.\nCoding guidelines \u0026nbsp; In general, run clang-format \u0026lt;your-file.cpp\u0026gt; before committing to ensure your changes follow our coding standards.\nLicense \u0026nbsp; By contributing your code, you agree to license your contribution under the BSD license\u0026nbsp; . By contributing to the documentation, you agree to license your contribution under the Creative Commons ( CC BY-NC 4.0\u0026nbsp; ) license."
      })
      .add(
      
      
      {
        id: 14,
        tag: "en",
        href: "/docs/about/credits/",
        title: "Credits",
        description: "OpenSees is fully open source and uses several open-source frameworks and libraries.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 15,
        tag: "en",
        href: "/docs/developing/",
        title: "Developing",
        description: "Details about the internals of OpenSees.",
        
        
        content: "Class Interface Specification \u0026nbsp; Classes may be categorized as follows:\nDomain: These classes describe the finite element model and store the results of an analysis on the model. The classes include Domain, Element, Node, Load, SP_Constraint, MP_Constraint, and their subclasses.\nAnalysis: These classes perform the analysis of the finite element model. The classes include the Analysis, ConstraintHandler, DOF_Numberer, SolutionAlgorithm, Integrator, FE_Element, DOF_Group and AnalysisModel classes, and their subclasses.\nComputational Classes: These classes allow for composing efficient computational strategies that take advantage of prolem features such as sparsity, symmetry, and parallelism. More specifically these include:\nSystem of Equation These include the abstract SystemOfEquation and Solver classes, and subclasses of these classes. These classes are provided for the solving of large scale systems of linear and eigenvalue equations.\nGraph These are classes used to provide information about nodal and elemental connectivity and sparsity of systems of equations. The classes include Graph, Vertex, GraphNumberer, GraphPartitioner, and their subclasses. There is no Edge class provided at present. In current design each Vertex stores in an ID the tag of all it\u0026rsquo;s adjacent Vertices. For graph numbering and partitioning this has proved sufficient.\nParallel Classes These facilitate the development of parallel object-oriented finite element programs, classes are provided for parallel programming. The classes in the framework support the aggregate programming model. The classes include Actor, Shadow, Message, MachineBroker, FEM_ObjectBroker, Channel, and their subclasses.\nRuntime Classes: These include the ModelNamespace and G3_Runtime classes. An analyst will interact with a ModelBuilder object, to create the Element, Node, Load and Constraint objects that define the model.\nOther/Utility Classes\nMatrix Classes: These include the classes Matrix, Vector and ID (integer array). These classes are used in the framework for passing information between objects in a safe manner, and for small scale numerical calculations in element formulation.\nData Storage These are classes used to store data. There are two abstract classes TaggedObjectStorage and FE_Datastore. Objects of type TaggedObjectStorage are used as containers to store and provide access to the TaggedObjects in memory during program execution. FE_Datastore objects are used to store/retrieve information from databases, containers which can permanently hold program data.\nVisualization Classes These are classes used to generate images of the model for the analyst. These classes include Renderer, ColorMap, and their subclasses.\nThis design allows for contributions in the fields of:\nElement and material modeling.\nSolution algorithms, integration procedures and constraint handling techniques.\nModel generation.\nNumerical analysis for solution of linear and eigenvalue problems.\nGraph theory for numbering and partitioning graphs.\nData structures for container classes and database.\nGraphics.\nMessage passing systems and load balancing in parallel environments.\nFrank McKenna and Gregory L. Fenves December 20, 1999"
      })
      .add(
      
      
      {
        id: 16,
        tag: "en",
        href: "/docs/library/docs/",
        title: "Docs",
        description: "The docs shortcode captures a code snippet from a supported input file.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 17,
        tag: "en",
        href: "/examples/example7/",
        title: "Dynamic Shell Analysis",
        description: "Transient analysis of a shell model.",
        
        
        content: "In this example a simple problem in shell dynamics is considered. The structure is a curved hoop shell structure that looks like the roof of a Safeway.\nExample7.tcl Example7.py Renderings are created from the script render.py, which uses the sees\u0026nbsp; Python package.\nModeling \u0026nbsp; For shell analysis, a typical shell element is defined as a surface in three dimensional space. Each node of a shell analysis has six degrees of freedom, three displacements and three rotations. Thus the model is defined with ndm=3ndm = 3 and ndf=6ndf = 6 .\nFor this model, a mesh is generated using the block2D command. The number of nodes in the local x-direction of the block is nx and the number of nodes in the local y-direction of the block is ny. The block2D generates nodes with tags 1,2,3,4, 5,7,9 such that the structure is curved in space.\nThe shell element is constructed using the ShellMITC4 formulation. An elastic membrane-plate material section model, appropriate for shell analysis, is constructed using the section command and the \u0026quot;ElasticMembranePlateSection\u0026quot; formulation. In this case, the elastic modulus E=3.0e3E = 3.0e3 , Poisson\u0026rsquo;s ratio ν=0.25\\nu = 0.25 , the thickness h=1.175h = 1.175 and the mass density per unit volume ρ=1.27\\rho = 1.27 Boundary conditions are applied using the fixZ command. In this case, all the nodes whose zz -coordiate is 0.00.0 have the boundary condition 1,1,1, 0,1,1: all degrees-of-freedom are fixed except rotation about the x-axis, which is free. The same boundary conditions are applied where the zz -coordinate is 40.040.0 .\nA solution algorithm of type Newton is used for the problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. Five static load steps are performed.\nFor initial gravity load analysis, a single load pattern with a linear time series and three vertical nodal loads are used. A scaled rendering of the deformed shape under gravity loading is shown below:\nDynamic Analysis \u0026nbsp; After the static analysis, the wipeAnalysis and remove loadPatern commands are used to remove the nodal loads and create a new analysis. The nodal displacements have not changed. However, with the external loads removed the structure is no longer in static equilibrium.\nThe integrator for the dynamic analysis if of type GeneralizedMidpoint with α=0.5\\alpha = 0.5 . This choice is uconditionally stable and energy conserving for linear problems. Additionally, this integrator conserves linear and angular momentum for both linear and non-linear problems. The dynamic analysis is performed using 250250 time increments with a time step Δt=0.50\\Delta t = 0.50 .\nThe results consist of the file Node.out, which contains a line for every time step. Each line contains the time and the vertical displacement at the upper center of the hoop structure. The time history is shown in the figure below.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 18,
        tag: "en",
        href: "/docs/library/example/",
        title: "Example",
        description: "The example shortcode displays a code example and renders a preview of the same input.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 19,
        tag: "en",
        href: "/examples/example1/",
        title: "Example 1: Linear Truss",
        description: "A finite element model of a simple truss is created, and static analysis is performed.",
        
        
        content: "\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e This example is of a linear-elastic three bar truss, as shown in the figure above, subject to static loads. The purpose of this example is to develop the basic requirements for performing finite element analysis with OpenSees. This includes the definition of nodes, materials, elements, loads and constraints.\nScripts for this example can be downloaded for either Python or Tcl:\nExample1.py Example1.tcl Model \u0026nbsp; We begin the simulation by creating a Model, which will manage the nodes, elements, loading and state. This is done through either Python or Tcl as follows:\nTcl Python model -ndm 2 -ndf 2 import opensees.openseespy as ops model = ops.Model(ndm=2, ndf=2) where we\u0026rsquo;ve specified 2 for the spatial dimension ndm, and 2 for the number of degrees of freedom ndf.\nNext we define the four nodes of the structural model by specifying a tag which identifies the node, and coordinates in the x−yx-y plane. In general, the node constructor must be passed ndm coordinates.\nTcl Python # Create nodes \u0026amp; add to domain # tag X Y node 1 0.0 0.0; node 2 144.0 0.0; node 3 168.0 0.0; node 4 72.0 96.0; # Create nodes # tag X Y model.node(1, 0.0, 0.0) model.node(2, 144.0, 0.0) model.node(3, 168.0, 0.0) model.node(4, 72.0, 96.0) The restraints at the nodes with reactions (ie, nodes 1, 2, and 3) are then defined.\nTcl Python # Set the boundary conditions # tag X Y fix 1 1 1; fix 2 1 1; fix 3 1 1; # set the boundary conditions # nodeID xRestrnt? yRestrnt? model.fix(1, 1, 1) model.fix(2, 1, 1) model.fix(3, 1, 1) Since the truss elements have the same elastic material, a single Elastic material object is created. The first argument assigns the tag 1 to the material, and the second specifies a Young\u0026rsquo;s modulus of 3000.\nTcl Python # Create Elastic material prototype uniaxialMaterial Elastic 1 3000; # Create Elastic material prototype model.uniaxialMaterial(\u0026#34;Elastic\u0026#34;, 1, 3000) Finally, define the elements. The syntax for creating the truss element requires the following arguments:\nthe element name, in this case always \u0026quot;Truss\u0026quot;, the element tag, in this case 1 through 3, the nodes that the element is connected to, the cross-sectional area, in this case 10.0 for element 1 and 5.0 for elements 2 and 3. the tag of the material assigned to the element, in this case always 1 Tcl Python element Truss 1 1 4 10.0 1; element Truss 2 2 4 5.0 1; element Truss 3 3 4 5.0 1; # Type tag nodes Area material model.element(\u0026#34;Truss\u0026#34;, 1, (1, 4), 10.0, 1 ) model.element(\u0026#34;Truss\u0026#34;, 2, (2, 4), 5.0, 1 ) model.element(\u0026#34;Truss\u0026#34;, 3, (3, 4), 5.0, 1 ) Loads \u0026nbsp; The final step before we can configure and run the analysis is to define some loading. In this case we have two point loads at the apex of the truss (node 4). In OpenSees, loads are assigned to load patterns, which define how loads are scaled with each load step. In Python, the simplest way to represent a nodal load is by a dictionary with node numbers as keys, and corresponding load vector as values. For the problem at hand, we want to apply a load to node 4 with 100 units in the xx direction, and -50 units in the yy direction; the corresponding definition is: Tcl Python set loads 4 100 -50 loads = 4: [100, -50] We then add a \u0026quot;Plain\u0026quot; load pattern to the model with these loads, and use the \u0026quot;Linear\u0026quot; option to specify that it should be increased linearly with each new load step. Tcl Python pattern Plain 1 \u0026#34;Linear\u0026#34; \u0026#34;load $loads\u0026#34; model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;, load=loads) Note that it is common to define the load data structure inside the call to the pattern function. This looks like:\nTcl Python pattern Plain 1 \u0026#34;Linear\u0026#34;  load 4 100 -50  model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;, load= 4: [100, -50] ) Analysis \u0026nbsp; Next we configure that analysis procedure. The model is linear, so we use a solution Algorithm of type Linear.\nTcl Python algorithm Linear; model.algorithm(\u0026#34;Linear\u0026#34;) Even though the solution is linear, we have to select a procedure for applying the load, which is called an Integrator. For this problem, a LoadControl integrator is selected, which advances the solution by incrementing the applied loads by a factor of 1.0 each time the analyze command is called.\nTcl Python integrator LoadControl 1.0; model.integrator(\u0026#34;LoadControl\u0026#34;, 1.0) The equations are formed using a banded system, so the System is BandSPD (banded, symmetric positive definite). This is a good choice for most moderate size models. The equations have to be numbered, so typically an RCM numberer object is used (for Reverse Cuthill-McKee). The constraints are most easily represented with a Plain constraint handler.\nOnce all the components of an analysis are defined, the Analysis itself is defined. For this problem a Static analysis is used.\nTcl Python analysis Static; model.analysis(\u0026#34;Static\u0026#34;) Finally, one analysis step is performed by invoking analyze: Tcl Python analyze 1 model.analyze(1) When the analysis is complete the state of node 4 and all three elements may be printed to the screen:\nTcl Python print node 4 print ele model.print(node=4) model.print(\u0026#34;ele\u0026#34;) Node: 4 Coordinates : 72 96 commitDisps: 0.530093 -0.177894 unbalanced Load: 100 -50 Element: 1 type: Truss iNode: 1 jNode: 4 Area: 10 Total Mass: 0 strain: 0.00146451 axial load: 43.9352 unbalanced load: -26.3611 -35.1482 26.3611 35.1482 Material: Elastic tag: 1 E: 3000 eta: 0 Element: 2 type: Truss iNode: 2 jNode: 4 Area: 5 Total Mass: 0 strain: -0.00383642 axial load: -57.5463 unbalanced load: -34.5278 46.0371 34.5278 -46.0371 Material: Elastic tag: 1 E: 3000 eta: 0 Element: 3 type: Truss iNode: 3 jNode: 4 Area: 5 Total Mass: 0 strain: -0.00368743 axial load: -55.3114 unbalanced load: -39.1111 39.1111 39.1111 -39.1111 Material: Elastic tag: 1 E: 3000 eta: 0For the node, displacements and loads are given. For the truss elements, the axial strain and force are provided along with the resisting forces in the global coordinate system.\nThe file example.out, specified in the recorder command, provides the nodal displacements for the xx and yy directions of node 4. The file consists of a single line:\n1.0 0.530093 -0.177894 The 1.01.0 corresponds to the load factor (pseudo time) in the model at which point the recorder was invoked. The 0.5300930.530093 and −0.177894-0.177894 correspond to the response at node 4 for the 1 and 2 degree-of-freedom. Note that if more analysis steps had been performed, the line would contain a line for every analysis step that completed successfully."
      })
      .add(
      
      
      {
        id: 20,
        tag: "en",
        href: "/examples/example4/",
        title: "Example 4: Multibay Two Story Frame",
        description: "A multi-bay reinforced concrete frame is investigated.",
        
        
        content: "Example 4.1 \u0026nbsp; This example is of a reinforced concrete multibay two story frame, as shown in Figure 1, subject to gravity loads. The files for this example are: Python Tcl \u0026lt;a href=\u0026quot;Example4.py\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example4.py\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; \u0026lt;a href=\u0026quot;Example4.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example4.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; A model of the frame shown in Figure 1 is created. The number of objects in the model is dependent on the parameter numBay. The (numBay + 1)*3 nodes are created, one column line at a time, with the node at the base of the columns fixed in all directions. Three materials are constructed, one for the concrete core, one for the concrete cover and one for the reinforcement steel. Three fiber discretized sections are then built, one for the exterior columns, one for the interior columns and one for the girders. Each of the members in the frame is modelled using nonlinear beam-column elements with 4 (nP) integration points and a linear geometric transformation object.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e For gravity loads, a single load pattern with a linear time series and two vertical nodal loads acting at the first and second floor nodes of each column line is used. The load at the lower level is twice that of the upper level and the load on the interior columns is twice that of the exterior columns.\nFor the lateral load analysis, a second load pattern with a linear time series is introduced after the gravity load analysis. Associated with this load pattern are two nodal loads acting on nodes 2 and 3, with the load level at node 3 twice that acting at node 2.\nThe integrator for the analysis will be LoadControl with a load step increment of 0.1. The constraints are enforced with a Plain constraint handler.\nOnce the components of the analysis have been defined, the analysis object is then created. For this problem a Static analysis is used and 10 steps are performed to load the model with the desired gravity load.\nAfter the gravity load analysis has been performed, the gravity loads are set to constant and the time in the domain is reset to 0.0. A new LoadControl integrator is now added. The new LoadControl integrator has an initial load step of 1.0, but this can vary between 0.02 and 2.0 depending on the number of iterations required to achieve convergence at each load step. 100 steps are then performed.\nThe output consists of the file Node41.out containing a line for each step of the lateral load analysis. Each line contains the load factor, the lateral displacements at nodes 2 and 3. A plot of the load-displacement curve for the frame is given in Figure 2.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 21,
        tag: "en",
        href: "/docs/library/file/",
        title: "File",
        description: "The file shortcode prints the full content of any given file with syntax highlighting.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 22,
        tag: "en",
        href: "/examples/example5/",
        title: "Frame with Diaphragms",
        description: "A three-dimensional reinforced concrete rigid frame, is subjected to bi-directional earthquake ground motion.",
        
        
        content: "A three-dimensional reinforced concrete rigid frame, is subjected to bi-directional earthquake ground motion.\nExample5.tcl RCsection.tcl Or for Python:\nExample5.py In both cases, the following ground motion records are required:\ntabasFN.txt tabasFP.txt Modeling \u0026nbsp; A model of the rigid frame shown in the figure below is created. The model consists of three stories and one bay in each direction. Rigid diaphragm multi-point constraints are used to enforce the rigid in-plane stiffness assumption for the floors. Gravity loads are applied to the structure and the 1978 Tabas acceleration records are the uniform earthquake excitations.\nNonlinear beam column elements are used for all members in the structure. The beam sections are elastic while the column sections are discretized by fibers of concrete and steel. Elastic beam column elements may have been used for the beam members; but, it is useful to see that section models other than fiber sections may be used in the nonlinear beam column element.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e Analysis \u0026nbsp; A solution Algorithm of type Newton is used for the nonlinear problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. The integrator for this analysis will be of type Newmark with a γ\\gamma of 0.25 and a β\\beta of 0.5. Due to the presence of the multi-point constraints, a Transformation constraint handler is used.\nOnce all the components of an analysis are defined, the Analysis itself is defined. For this problem a Transient analysis is used. 2000 steps are performed with a time step of 0.01.\nPost-Processing \u0026nbsp; The nodal displacements at nodes 9, 14, and 19 (the retained nodes for the rigid diaphragms) will be stored in the file node51.out for post-processing.\nThe results consist of the file node.out, which contains a line for every time step. Each line contains the time and the horizontal and vertical displacements at the diaphragm retained nodes (9, 14 and 19) i.e. time Dx9 Dy9 Dx14 Dy14 Dx19 Dy19. The horizontal displacement time history of the first floor diaphragm node 9 is shown in the figure below. Notice the increase in period after about 10 seconds of earthquake excitation, when the large pulse in the ground motion propogates through the structure. The displacement profile over the three stories shows a soft-story mechanism has formed in the first floor columns. The numerical solution converges even though the drift is ≈20%\\approx 20 \\% . The inclusion of P−ΔP-\\Delta effects shows structural collapse under such large drifts.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 23,
        tag: "en",
        href: "/docs/library/icon/",
        title: "Icon",
        description: "Use the icon shortcode to add a Font Awesome icon with ease.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 24,
        tag: "en",
        href: "/docs/advanced-settings/icons/",
        title: "Icons",
        description: "Configure secure access to icons from Bootstrap and Font Awesome.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 25,
        tag: "en",
        href: "/docs/library/image/",
        title: "Image",
        description: "Use the image shortcode to display a responsive image with a specific aspect ratio.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 26,
        tag: "en",
        href: "/examples/example3/",
        title: "Inelastic Plane Frame",
        description: "Nonlinear analysis of a concrete portal frame.",
        
        
        content: "\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e This set of examples investigates the nonlinear analysis of a reinforced concrete frame. The nonlinear beam column element with a fiber discretization of the cross section is used in the model. The files for this example are: Python Tcl \u0026lt;a href=\u0026quot;portal.py\u0026quot;\u0026gt;\u0026lt;code\u0026gt;portal.py\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; \u0026lt;a href=\u0026quot;portal.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;portal.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; These files define the following functions:\nFunction Description create_portal Creates a model of a portal frame gravity_analysis Performs a gravity analysis on a model pushover_analysis Performs a pushover analysis on a model transient_analysis Performs a transient analysis on a model create_portal \u0026nbsp; The function create_portal creates a model representing the portal frame in the figure above. The model consists of four nodes, two nonlinear beam-column elements modeling the columns and an elastic beam element to model the girder. For the column elements a section, identical to the section used in Example 2, is created using steel and concrete fibers.\nBegin with nodes and boundary conditions Python Tcl # create ModelBuilder (with two-dimensions and 3 DOF/node) model = ops.Model(ndm=2, ndf=3) # Create nodes # ------------ # create nodes \u0026amp; add to Domain - command: node nodeId xCrd yCrd model.node(1, 0.0, 0.0) model.node(2, width, 0.0) model.node(3, 0.0, height) model.node(4, width, height) # set the boundary conditions - command: fix nodeID uxRestrnt? uyRestrnt? rzRestrnt? model.fix(1, 1, 1, 1) model.fix(2, 1, 1, 1) set width 360 set height 144 model basic -ndm 2 -ndf 3 # Create nodes # tag X Y node 1 0.0 0.0 node 2 $width 0.0 node 3 0.0 $height node 4 $width $height # Fix supports at base of columns # tag DX DY RZ fix 1 1 1 1 fix 2 1 1 1 Next define the materials\nPython Tcl # Define materials for nonlinear columns # ------------------------------------------ # CONCRETE tag f\u0026#39;c ec0 f\u0026#39;cu ecu # Core concrete (confined) model.uniaxialMaterial(\u0026#34;Concrete01\u0026#34;, 1, -6.0, -0.004, -5.0, -0.014) # Cover concrete (unconfined) model.uniaxialMaterial(\u0026#34;Concrete01\u0026#34;, 2, -5.0, -0.002, -0.0, -0.006) # STEEL # Reinforcing steel fy = 60.0; # Yield stress E = 30000.0; # Young\u0026#39;s modulus # tag fy E b model.uniaxialMaterial(\u0026#34;Steel01\u0026#34;, 3, fy, E, 0.01) # Define materials for nonlinear columns # ------------------------------------------ # CONCRETE tag f\u0026#39;c ec0 f\u0026#39;cu ecu # Core concrete (confined) uniaxialMaterial Concrete01 1 -6.0 -0.004 -5.0 -0.014 # Cover concrete (unconfined) uniaxialMaterial Concrete01 2 -5.0 -0.002 0.0 -0.006 # STEEL # Reinforcing steel set fy 60.0; # Yield stress set E 30000.0; # Young\u0026#39;s modulus # tag fy E0 b uniaxialMaterial Steel01 3 $fy $E 0.01 Define a cross section for the columns Python Tcl # Define cross-section for nonlinear columns # ------------------------------------------ # set some parameters colWidth = 15.0 colDepth = 24.0 cover = 1.5 As = 0.6 # area of no. 7 bars # some variables derived from the parameters y1 = colDepth/2.0 z1 = colWidth/2.0 model.section(\u0026#34;Fiber\u0026#34;, 1) # Add the concrete core fibers model.patch(\u0026#34;rect\u0026#34;, 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover, section=1) # Add the concrete cover fibers (top, bottom, left, right) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, z1-cover, y1, z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, -z1, y1, cover-z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, -y1, cover-z1, cover-y1, z1-cover, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, y1-cover, cover-z1, y1, z1-cover, section=1) # Add the reinforcing fibers (left, middle, right, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 2, As, 0.0, z1-cover, 0.0, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, cover-y1, z1-cover, cover-y1, cover-z1, section=1) # Define cross-section for nonlinear columns # ------------------------------------------ # set some parameters set colWidth 15 set colDepth 24 set cover 1.5 set As 0.60; # area of no. 7 bars # some variables derived from the parameters set y1 [expr $colDepth/2.0] set z1 [expr $colWidth/2.0] section Fiber 1  # Add the concrete core fibers patch rect 1 10 1 [expr $cover-$y1] [expr $cover-$z1] [expr $y1-$cover] [expr $z1-$cover] # Add the concrete cover fibers (top, bottom, left, right) patch rect 2 10 1 [expr -$y1] [expr $z1-$cover] $y1 $z1 patch rect 2 10 1 [expr -$y1] [expr -$z1] $y1 [expr $cover-$z1] patch rect 2 2 1 [expr -$y1] [expr $cover-$z1] [expr $cover-$y1] [expr $z1-$cover] patch rect 2 2 1 [expr $y1-$cover] [expr $cover-$z1] $y1 [expr $z1-$cover] # Add the reinforcing fibers (left, middle, right) layer straight 3 3 $As [expr $y1-$cover] [expr $z1-$cover] [expr $y1-$cover] [expr $cover-$z1] layer straight 3 2 $As 0.0 [expr $z1-$cover] 0.0 [expr $cover-$z1] layer straight 3 3 $As [expr $cover-$y1] [expr $z1-$cover] [expr $cover-$y1] [expr $cover-$z1]  gravity_analysis \u0026nbsp; We now implement a function called gravity_analysis which takes the instance of Model returned by create_portal, and proceeds to impose gravity loads and perform a static analysis. Its use will look like:\nPython Tcl # Create the model model = create_portal() # perform analysis under gravity loads status = gravity_analysis(model) create_portal; gravity_analysis; A single load pattern with a linear time series is created with two vertical nodal loads acting at nodes 3 and 4:\nPython Tcl model.pattern(\u0026#34;Plain\u0026#34;, 1, \u0026#34;Linear\u0026#34;, loads= # nodeID xForce yForce zMoment 3: [ 0.0, -P, 0.0], 4: [ 0.0, -P, 0.0] ) The model contains material non-linearities, so a solution algorithm of type Newton is used. The solution algorithm uses a ConvergenceTest which tests convergence of the equilibrium solution with the norm of the displacement increment vector. For this nonlinear problem, the gravity loads are applied incrementally until the full load is applied. To achieve this, a LoadControl integrator which advances the solution with an increment of 0.1 at each load step is used. The equations are formed using a banded storage scheme, so the System is BandGeneral. The equations are numbered using an RCM (reverse Cuthill-McKee) numberer. The constraints are enforced with a Plain constraint handler.\nOnce all the components of an analysis are defined, the Analysis object itself is created. For this problem a Static Analysis object is used. To achieve the full gravity load, 10 load steps are performed.\nAt end of analysis, the state at nodes 3 and 4 is output. The state of element 1 is also output.\nFor the two nodes, displacements and loads are given. For the beam-column elements, the element end forces in the local system are provided.\nThe nodeGravity.out file contains ten lines, each line containing 7 entries. The first entry is time in the domain at end of the load step. The next 3 entries are the displacements at node 3, and the final 3 entries the displacements at node 4.\npushover_analysis \u0026nbsp; In this example the nonlinear reinforced concrete portal frame which has undergone the gravity load analysis of Example 3.1 is now subjected to a pushover analysis.\nAfter performing the gravity load analysis on the model, the time in the domain is reset to 0.0 and the current value of all loads acting are held constant. A new load pattern with a linear time series and horizontal loads acting at nodes 3 and 4 is then added to the model.\nThe static analysis used to perform the gravity load analysis is modified to take a new DisplacementControl integrator. At each new step in the analysis the integrator will determine the load increment necessary to increment the horizontal displacement at node 3 by 0.1 in. 60 analysis steps are performed in this new analysis.\nFor this analysis the nodal displacements at nodes 3 and 4 will be stored in the file nodePushover.out for post-processing. In addition, the end forces in the local coordinate system for elements 1 and 2 will be stored in the file elePushover.out. At the end of the analysis, the state of node 3 is printed to the screen.\nIn addition to what is displayed on the screen, the file node32.out and ele32.out have been created by the script. Each line of node32.out contains the time, DX, DY and RZ for node 3 and DX, DY and RZ for node 4 at the end of an iteration. Each line of eleForce.out contains the time, and the element end forces in the local coordinate system. A plot of the load-displacement relationship at node 3 is shown in the figure below.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e transient_analysis \u0026nbsp; The concrete frame which has undergone the gravity load analysis of Example 3.1 is now subjected to a uniform earthquake excitation.\nAfter performing the gravity load analysis, the time in the domain is reset to 0.0 and the time series for all active loads is set to constant. This prevents the gravity load from being scaled with each step of the dynamic analysis.\nPython Tcl model.loadConst(time=0.0) loadConst -time 0.0 Mass terms are added to nodes 3 and 4. A new uniform excitation load pattern is created. The excitation acts in the horizontal direction and reads the acceleration record and time interval from the file ARL360.g3. The file ARL360.g3 is created from the PEER Strong Motion Database ( http://peer.berkeley.edu/smcat/\u0026nbsp; ) record ARL360.at2 using the Tcl procedure ReadSMDFile contained in the file ReadSMDFile.tcl.\nThe static analysis object and its components are first deleted so that a new transient analysis object can be created.\nA new solution Algorithm of type Newton is then created. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the displacement increment vector. The integrator for this analysis will be of type Newmark with a γ=0.25\\gamma = 0.25 and β=0.5\\beta = 0.5 .\nThe integrator will add some stiffness proportional damping to the system, the damping term will be based on the last committed stifness of the elements, i.e. C=acKcommitC = a_c K_\\textcommit with ac=0.000625a_c = 0.000625 .\nThe equations are formed using a banded storage scheme, so the System is BandGeneral. The equations are numbered using an RCM (reverse Cuthill-McKee) numberer. The constraints are enforced with a Plain constraint handler.\nOnce all the components of an analysis are defined, the Analysis object itself is created. For this problem a Transient Analysis object is used. 2000 time steps are performed with a time step of 0.01.\nIn addition to the transient analysis, two eigenvalue analysis are performed on the model. The first is performed after the gravity analysis and the second after the transient analysis.\nFor this analysis the nodal displacenments at Nodes 3 and 4 will be stored in the file nodeTransient.out for post-processing. In addition the section forces and deformations for the section at the base of column 1 will also be stored in two seperate files. The results of the eigenvalue analysis will be displayed on the screen.\nGravity load analysis completed eigen values at start of transient: 2.695422e+02 1.750711e+04 Transient analysis completed SUCCESSFULLY eigen values at start of transient: 1.578616e+02 1.658481e+04 Node: 3 Coordinates : 0 144 commitDisps: -0.0464287 -0.0246641 0.000196066 Velocities : -0.733071 1.86329e-05 0.00467983 commitAccels: -9.13525 0.277302 38.2972 unbalanced Load: -3.9475 -180 0 Mass : 0.465839 0 0 0 0.465839 0 0 0 0 Eigenvectors: -1.03587 -0.0482103 -0.00179081 0.00612275 0.00663473 3.21404e-05 The two eigenvalues for the eigenvalue analysis are printed to the screen. The state of node 3 at the end of the analysis is also printed. The information contains the last committed displacements, velocities and accelerations at the node, the unbalanced nodal forces and the nodal masses. In addition, the eigenvector components of the eigenvector pertaining to the node 3 is also displayed.\nIn addition to the contents displayed on the screen, three files have been created. Each line of nodeTransient.out contains the domain time, and DX, DY and RZ for node 3. Plotting the first and second columns of this file the lateral displacement versus time for node 3 can be obtained as shown in the figure below. Each line of the files ele1secForce.out and ele1secDef.out contain the domain time and the forces and deformations for section 1 (the base section) of element 1. These can be used to generate the moment-curvature time history of the base section of column 1 as shown below.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e \u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 27,
        tag: "en",
        href: "/docs/getting-started/introduction/",
        title: "Introduction",
        description: "Get started with OpenSees.",
        
        
        content: "opensees is a Python package that provides an intuitive API for nonlinear finite element analysis, implemented in C++ through the OpenSees framework. OpenSees features state-of-the-art finite element formulations and solution algorithms, including mixed formulations for beams and solids, over 200 material models, and an extensive collection of continuation algorithms to solve highly nonlinear problems.\nInstallation \u0026nbsp; In order to install opensees just run the command:\npython -m pip install opensees Running OpenSees \u0026nbsp; The opensees package can be used in three ways:\nPython Module The opensees.openseespy Python module implements the API that has been developed by Oregon State. Command line interface An interactive Tcl interpreter can be started by invoking the module as follows from the command line:\npython -m opensees --help Interactive Interpreter An interactive Tcl interpreter can be started by invoking the module as follows from the command line:\npython -m opensees"
      })
      .add(
      
      
      {
        id: 28,
        tag: "en",
        href: "/docs/library/kbd/",
        title: "Kbd",
        description: "Use the kbd shortcode to show a keyboard input element.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 29,
        tag: "en",
        href: "/docs/configuration/layout/",
        title: "Layout",
        description: "Hinode uses a grid-based, responsive design for the home page, single pages and list pages.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 30,
        tag: "en",
        href: "/docs/about/license/",
        title: "License",
        description: "OpenSeesRT's open-source license for the codebase and documentation.",
        
        
        content: "Codebase \u0026nbsp; The codebase of OpenSeesRT is open source under the conditions of the MIT license\u0026nbsp; and is copyright © 2024 by Mark Dumay. In short, the MIT license allows you to use the OpenSeesRT codebase for both personal and commercial use, as long as you include the original license and copyright notice. Licensed works, modifications, and larger works may be distributed under different terms and without source code. No liability or warranty is given.\nDocumentation \u0026nbsp; The documentation of OpenSeesRT is licensed under the Creative Commons ( CC BY-NC 4.0\u0026nbsp; ) license. This includes all files within the repository\u0026rsquo;s /content and /exampleSite/content folders and their children, as well as the \u0026ldquo;README\u0026rdquo; in the repository root. The license allows you to share and adapt the materials, as long as you give appropriate credit and do not use the materials for commercial purposes. No warranties are given. p"
      })
      .add(
      
      
      {
        id: 31,
        tag: "en",
        href: "/docs/library/link/",
        title: "Link",
        description: "Use the link shortcode to add a managed link to your page content.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 32,
        tag: "en",
        href: "/docs/getting-started/modeling/",
        title: "Modeling",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 33,
        tag: "en",
        href: "/docs/advanced-settings/module-development/",
        title: "Module development",
        description: "Develop your own Hugo modules compatible with Hinode.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 34,
        tag: "en",
        href: "/examples/example2/",
        title: "Moment-Curvature Analysis",
        description: "A reinforced concrete cross-section is modeled using a fiber section,  and a moment-curvature analysis is performed.",
        
        
        content: "This example performs a moment-curvature analysis of a reinforced concrete section which is represented by a fiber discretization. Because we are only interested in the response quantities of the cross section, a zero-length element is used to wrap the cross section.\nModeling \u0026nbsp; The figure below shows the fiber discretization for the section. The files for this example are: Python Tcl \u0026lt;a href=\u0026quot;Example2.py\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example2.py\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; \u0026lt;a href=\u0026quot;Example2.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;Example2.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; \u0026lt;a href=\u0026quot;MomentCurvature.tcl\u0026quot;\u0026gt;\u0026lt;code\u0026gt;MomentCurvature.tcl\u0026lt;/code\u0026gt;\u0026lt;/a\u0026gt;\u0026lt;/li\u0026gt; The model consists of two nodes and a ZeroLengthSection element. A depiction of the element geometry is shown in figure zerolength. The drawing on the left of figure zerolength shows an edge view of the element where the local zz -axis, as seen on the right side of the figure and in figure rcsection0, is coming out of the page. Node 1 is completely restrained, while the applied loads act on node 2. A compressive axial load, PP , of 180180 kips is applied to the section during the moment-curvature analysis.\nA fiber section is created by grouping various patches and layers:\nNote in Python you must pass the section tag when calling patch and layer\nPython Tcl model.section(\u0026#34;Fiber\u0026#34;, 1) # Create the concrete core fibers model.patch(\u0026#34;rect\u0026#34;, 1, 10, 1, cover-y1, cover-z1, y1-cover, z1-cover, section=1) # Create the concrete cover fibers (top, bottom, left, right, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, z1-cover, y1, z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 10, 1, -y1, -z1, y1, cover-z1, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, -y1, cover-z1, cover-y1, z1-cover, section=1) model.patch(\u0026#34;rect\u0026#34;, 2, 2, 1, y1-cover, cover-z1, y1, z1-cover, section=1) # Create the reinforcing fibers (left, middle, right, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, y1-cover, z1-cover, y1-cover, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 2, As, 0.0, z1-cover, 0.0, cover-z1, section=1) model.layer(\u0026#34;straight\u0026#34;, 3, 3, As, cover-y1, z1-cover, cover-y1, cover-z1, section=1) section Fiber 1  # Create the concrete core fibers patch rect 1 10 1 [expr $cover-$y1] [expr $cover-$z1] [expr $y1-$cover] [expr $z1-$cover] # Create the concrete cover fibers (top, bottom, left, right) patch rect 2 10 1 [expr -$y1] [expr $z1-$cover] $y1 $z1 patch rect 2 10 1 [expr -$y1] [expr -$z1] $y1 [expr $cover-$z1] patch rect 2 2 1 [expr -$y1] [expr $cover-$z1] [expr $cover-$y1] [expr $z1-$cover] patch rect 2 2 1 [expr $y1-$cover] [expr $cover-$z1] $y1 [expr $z1-$cover] # Create the reinforcing fibers (left, middle, right) layer straight 3 3 $As [expr $y1-$cover] [expr $z1-$cover] [expr $y1-$cover] [expr $cover-$z1] layer straight 3 2 $As 0.0 [expr $z1-$cover] 0.0 [expr $cover-$z1] layer straight 3 3 $As [expr $cover-$y1] [expr $z1-$cover] [expr $cover-$y1] [expr $cover-$z1]  For the zero length element, a section discretized by concrete and steel is created to represent the resultant behavior. UniaxialMaterial objects are created to define the fiber stress-strain relationships: confined concrete in the column core, unconfined concrete in the column cover, and reinforcing steel.\nThe dimensions of the fiber section are shown in figure rcsection0. The section depth is 24 inches, the width is 15 inches, and there are 1.5 inches of cover around the entire section. Strong axis bending is about the section zz -axis. In fact, the section zz -axis is the strong axis of bending for all fiber sections in planar problems. The section is separated into confined and unconfined concrete regions, for which separate fiber discretizations will be generated. Reinforcing steel bars will be placed around the boundary of the confined and unconfined regions. The fiber discretization for the section is shown in figure rcsection4.\nAnalysis \u0026nbsp; The section analysis is performed by the procedure moment_curvature defined in the file MomentCurvature.tcl for Tcl, and Example2.1.py for Python. The arguments to the procedure are the tag secTag of the section to be analyzed, the axial load axialLoad applied to the section, the maximum curvature maxK, and the number numIncr of displacement increments to reach the maximum curvature.\nThe output for the moment-curvature analysis will be the section forces and deformations, stored in the file section1.out. In addition, an estimate of the section yield curvature is printed to the screen.\nIn the moment_curvature procedure, the nodes are defined to be at the same geometric location and the ZeroLengthSection element is used. A single load step is performed for the axial load, then the integrator is changed to DisplacementControl to impose nodal displacements, which map directly to section deformations. A reference moment of 1.0 is defined in a Linear time series. For this reference moment, the DisplacementControl integrator will determine the load factor needed to apply the imposed displacement. A node recorder is defined to track the moment-curvature results. The load factor is the moment, and the nodal rotation is in fact the curvature of the element with zero thickness.\nThe expected output is:\nEstimated yield curvature: 0.000126984126984 The file section1.out contains for each committed state a line with the load factor and the rotation at node 3. This can be used to plot the moment-curvature relationship as shown in figure momcurv."
      })
      .add(
      
      
      {
        id: 35,
        tag: "en",
        href: "/docs/library/navbar/",
        title: "Navbar",
        description: "Use the navbar shortcode to display a navigation header with a toggler.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 36,
        tag: "en",
        href: "/docs/library/navs-and-tabs/",
        title: "Navs and tabs",
        description: "Use the nav shortcode to show a group of multiple tab panes.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 37,
        tag: "en",
        href: "/docs/advanced-settings/overview/",
        title: "Overview",
        description: "Configure and customize Hinode to your liking using modules, npm, and mounted folders.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 38,
        tag: "en",
        href: "/docs/advanced-settings/partial-development/",
        title: "Partial development",
        description: "Develop custom partials and shortcodes following Hinode's coding conventions.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 39,
        tag: "en",
        href: "/docs/getting-started/python/",
        title: "Python",
        description: "",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 40,
        tag: "en",
        href: "/docs/library/release/",
        title: "Release",
        description: "Use the release shortcode to indicate the availability of a specific feature in a tagged release.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 41,
        tag: "en",
        href: "/releases/",
        title: "Releases",
        description: "A chronological overview of key releases since the initial launch of Hinode.",
        
        
        content: "The timeline below captures the significant changes since the initial release of Hinode in April, 2022. Visit GitHub for a full overview of all Hinode releases\u0026nbsp; , including features, bug fixes, and dependency upgrades.\nRender hooks v0.26.0 August 15, 2024\nThis release includes support for markdown links and markdown images. Hinode will invoke the relevant partials, so they will have the same behavior and styling as their counterparts. This release also includes support for server-side math rendering as introduced by Hugo v0.132.0\u0026nbsp; .\nScript bundle localization v0.25.0 August 2, 2024\nHinode includes search support out of the box. To limit the bundle size, the search index now includes entries for the current translation only. To enable localization, the module configuration includes a new parameter localize. By default, the FlexSearch module sets localization to true.\nInitial launch v0.1 April 13, 2022\nInspired by Blist and Doks, this release introduces Hinode - a modern blog and documentation theme for Hugo. By taking advantage of npm, the used dependencies are easily tracked and updated. Powered by Bootstrap, the generated website is responsive and brings many common UI elements. Hinode wraps many of these elements in a shortcode to simplify their usage.\nRender hooks v0.26.0 August 15, 2024\nThis release includes support for markdown links and markdown images. Hinode will invoke the relevant partials, so they will have the same behavior and styling as their counterparts. This release also includes support for server-side math rendering as introduced by Hugo v0.132.0\u0026nbsp; .\nScript bundle localization v0.25.0 August 2, 2024\nHinode includes search support out of the box. To limit the bundle size, the search index now includes entries for the current translation only. To enable localization, the module configuration includes a new parameter localize. By default, the FlexSearch module sets localization to true.\nInitial launch v0.1 April 13, 2022\nInspired by Blist and Doks, this release introduces Hinode - a modern blog and documentation theme for Hugo. By taking advantage of npm, the used dependencies are easily tracked and updated. Powered by Bootstrap, the generated website is responsive and brings many common UI elements. Hinode wraps many of these elements in a shortcode to simplify their usage."
      })
      .add(
      
      
      {
        id: 42,
        tag: "en",
        href: "/docs/advanced-settings/scripts/",
        title: "Scripts",
        description: "Automatically bundle local and external JavaScript files into a single file.",
        
        
        content: "Hinode bundles local JavaScript files and JavaScript files defined in a core module into a single file. By utilizing Hugo modules, external JavaScript files are automatically ingested and kept up to date.\nBuild pipeline \u0026nbsp; Hinodes uses Hugo modules and mounted folders to create a flexible virtual file system that is automatically kept up to date. Review the overview for a detailed explanation. The build pipeline of the JavaScript files consists of four steps.\nMount the JavaScript files maintained within the core modules\nMake JavaScripts defined in core modules available by mounting them into a separate assets/js/modules/MODULE NAME/ folder for each module. Adjust the mount points in config/_default/hugo.toml as needed.\nAdd the local JavaScript files\nAdd the local JavaScript files to the assets/js folder with a recognizable filename.\nBundle the JavaScript files\nThe partial partials/footer/scripts.html bundles all files that end with .js recursively into a single file called js/main.bundle.js. The files are processed in the order of the configured core modules and are sorted alphabetically within each module. JavaScript files defined in the current repository are added last, sorted alphabetically too. In production mode, the bundled output is minified and linked to with a fingerprint\u0026nbsp; .\nLink to the JavaScript in the base layout\nHinode\u0026rsquo;s base layout layouts/_default/baseof.html imports the bundled JavaScript file in the footer. The file is cached to improve performance.\nCritical files \u0026nbsp; [...] \u0026lt;!doctype html\u0026gt; \u0026lt;html lang=\u0026#34; .Site.Language.Lang \u0026#34; class=\u0026#34;no-js\u0026#34;\u0026gt; \u0026lt;head\u0026gt;  block \u0026#34;head\u0026#34; .  end - \u0026lt;/head\u0026gt; \u0026lt;body\u0026gt; - if site.Params.main.enableDarkMode - - partial \u0026#34;footer/scripts.html\u0026#34; (dict \u0026#34;filename\u0026#34; \u0026#34;js/critical.bundle.js\u0026#34; \u0026#34;match\u0026#34; \u0026#34;js/critical/**.js\u0026#34; \u0026#34;page\u0026#34; .) - - end - [...] \u0026lt;/body\u0026gt; \u0026lt;/html\u0026gt; Optional module files \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 43,
        tag: "en",
        href: "/examples/example6/",
        title: "Simply Supported Solid Beam",
        description: "In this example a simply supported beam is modelled with two dimensional solid elements. The example is implemented in both Tcl and Python:\nExample6.tcl Example6.py Each node of the analysis has two displacement degrees of freedom. Thus the model is defined with ndm = 2 and ndf = 2.\n",
        
        
        content: "In this example a simply supported beam is modelled with two dimensional solid elements. The example is implemented in both Tcl and Python:\nExample6.tcl Example6.py Each node of the analysis has two displacement degrees of freedom. Thus the model is defined with ndm = 2 and ndf = 2.\nA mesh is generated using the block2D command. The number of nodes in the local xx -direction of the block is nxnx and the number of nodes in the local yy -direction of the block is nyny . The block2D generation nodes 1,2,3,4 are prescribed to define the two dimensional domain of the beam, which is of size 40×1040\\times10 .\nThree different quadrilateral elements can be used for the analysis. These may be created using the names \u0026quot;BbarQuad\u0026quot;, \u0026quot;EnhancedQuad\u0026quot; or \u0026quot;Quad\u0026quot;. This is a plane strain problem. An elastic isotropic material is used.\nFor initial gravity load analysis, a single load pattern with a linear time series and two vertical nodal loads are used.\nA solution algorithm of type Newton is used for the problem. The solution algorithm uses a ConvergenceTest which tests convergence on the norm of the energy increment vector. Ten static load steps are performed.\nFollowing the static analysis, the wipeAnalysis and remove loadPatern commands are used to remove the nodal loads and create a new analysis. The nodal displacements have not changed. However, with the external loads removed the structure is no longer in static equilibrium.\nThe integrator for the dynamic analysis if of type GeneralizedMidpoint with α=0.5\\alpha = 0.5 . This choice is uconditionally stable and energy conserving for linear problems. Additionally, this integrator conserves linear and angular momentum for both linear and non-linear problems. The dynamic analysis is performed using 100100 time increments with a time step Δt=0.50\\Delta t = 0.50 .\nThe results consist of the file Node.out, which contains a line for every time step. Each line contains the time and the vertical displacement at the bottom center of the beam. The time history is shown in Figure 1.\n\u003c?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?\u003e"
      })
      .add(
      
      
      {
        id: 44,
        tag: "en",
        href: "/docs/advanced-settings/styles/",
        title: "Styles",
        description: "Use extensible Sass files to generate the stylesheets for your website.",
        
        
        content: ""
      })
      .add(
      
      
      {
        id: 45,
        tag: "en",
        href: "/docs/library/sub/",
        title: "Sub",
        description: "Use the sub shortcode to display text in subscript.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 46,
        tag: "en",
        href: "/docs/library/sup/",
        title: "Sup",
        description: "Use the sup shortcode to display text in superscript.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 47,
        tag: "en",
        href: "/docs/library/table/",
        title: "Table",
        description: "Use the table shortcode to make your Markdown table responsive.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 48,
        tag: "en",
        href: "/docs/library/timeline/",
        title: "Timeline",
        description: "Use the timeline shortcode to show items ordered on a vertical timelime.",
        
        
        content: "Overview \u0026nbsp;"
      })
      .add(
      
      
      {
        id: 49,
        tag: "en",
        href: "/docs/library/tooltip/",
        title: "Tooltip",
        description: "Use the tooltip shortcode to display a tooltip for a hyperlink.",
        
        
        content: ""
      })
      ;
  

  search.addEventListener('input', showResults, true);
}
  
function hideSuggestions(e) {
  var isClickInsideElement = suggestions.contains(e.target);

  if (!isClickInsideElement) {
    suggestions.classList.add('d-none')
    if (background !== null ) {
      background.style.setProperty('--image-opacity', '0.1')
    }
  }
}

/*
Source:
  - https://raw.githubusercontent.com/h-enk/doks/master/assets/js/index.js
*/
function inputFocus(e) {
  if (e.ctrlKey && e.key === '/' ) {
    e.preventDefault();
    search.focus();
  }
  if (e.key === 'Escape' ) {
    search.blur();
    suggestions.classList.add('d-none');
  }
}

/*
Source:
  - https://dev.to/shubhamprakash/trap-focus-using-javascript-6a3
*/
function suggestionFocus(e) {
  const suggestionsHidden = suggestions.classList.contains('d-none');
  if (suggestionsHidden) return;

  const focusableSuggestions= [...suggestions.querySelectorAll('a')];
  if (focusableSuggestions.length === 0) return;

  const index = focusableSuggestions.indexOf(document.activeElement);

  if (e.key === "ArrowUp") {
    e.preventDefault();
    const nextIndex = index > 0 ? index - 1 : 0;
    focusableSuggestions[nextIndex].focus();
  }
  else if (e.key === "ArrowDown") {
    e.preventDefault();
    const nextIndex= index + 1 < focusableSuggestions.length ? index + 1 : index;
    focusableSuggestions[nextIndex].focus();
  }
}
  
/*
Source:
  - https://github.com/nextapps-de/flexsearch#index-documents-field-search
  - https://raw.githack.com/nextapps-de/flexsearch/master/demo/autocomplete.html
*/
function showResults() {
  const maxResult = 5;
  var searchQuery = this.value;
  // filter the results for the currently tagged language
  const lang = document.documentElement.lang;
  var results = null;
  if (searchQuery) {
    results = index.search(searchQuery, { index: ['title', 'description', 'content'], limit: maxResult, tag: lang, enrich: true });
    if (background !== null) {
      background.style.setProperty('--image-opacity', '0')
    }
  } else {
    if (background !== null) {
      background.style.setProperty('--image-opacity', '0.1')
    }
  }

  // flatten results since index.search() returns results for each indexed field
  const flatResults = new Map(); // keyed by href to dedupe results
  if (results !== null) {
    for (const result of results.flatMap(r => r.result)) {
      if (flatResults.has(result.doc.href)) continue;
      flatResults.set(result.doc.href, result.doc);
    }
  }

  suggestions.innerHTML = "";
  suggestions.classList.remove('d-none');
  
  // inform user that no results were found
  if (flatResults.size === 0 && searchQuery) {
    const msg = suggestions.dataset.noResults;
    const noResultsMessage = document.createElement('div')
    noResultsMessage.innerHTML = `${msg} "<strong>${searchQuery}</strong>"`
    noResultsMessage.classList.add("suggestion__no-results");
    suggestions.appendChild(noResultsMessage);
    return;
  }

  // construct a list of suggestions
  for (const [href, doc] of flatResults) {
    const entry = document.createElement('div');
    suggestions.appendChild(entry);

    const a = document.createElement('a');
    a.href = href;
    entry.appendChild(a);

    const title = document.createElement('span');
    title.classList.add('text-start');
    title.textContent = doc.title;
    title.classList.add("suggestion__title");
    a.appendChild(title);

    const description = document.createElement('span');
    description.textContent = doc.description;
    description.classList.add("suggestion__description");
    a.appendChild(description);

    suggestions.appendChild(entry);

    if (suggestions.childElementCount == maxResult) break;
  }
}
  
if (search !== null && suggestions !== null) {
  document.addEventListener('keydown', inputFocus);
  document.addEventListener('keydown', suggestionFocus);  
  document.addEventListener('click', hideSuggestions);
  initIndex();
}

const searchModal = document.getElementById('search-modal')
if (searchModal !== null) {
  searchModal.addEventListener('shown.bs.modal', function () {
    const searchInput = document.getElementById('search-input-modal')
    if (searchInput !== null) {
      searchInput.focus({ focusVisible: true })
    }
  })
}

;
document.querySelectorAll('.dynamic-svg').forEach((placeholder) => {
  placeholder.onload = function () {
    const container = placeholder.parentElement
    const doc = placeholder.contentDocument
    const attr = placeholder.getAttribute('data-class')
    const style = placeholder.getAttribute('data-style')

    if (container !== null && doc !== null) {
      const svg = doc.querySelector('svg')
      if (svg !== null) {
        svg.setAttribute('class', 'svg-inline--fa ' + (attr || ''))
        svg.setAttribute('fill', 'currentcolor')
        svg.setAttribute('aria-hidden', 'true')
        svg.setAttribute('role', 'img')
        if (style !== null && style !== '') {
          svg.setAttribute('style', style)
        }
        svg.removeAttribute('height')
        svg.removeAttribute('width')
        container.innerHTML = ''
        container.appendChild(svg)
      }
    }
  }
})

;
const fixed = true
const navbar = document.querySelector('.navbar')
const togglers = document.querySelectorAll('.main-nav-toggler')
const modeSelectors = document.querySelectorAll('.switch-mode-collapsed')
const colorsBG = ['body', 'secondary', 'tertiary']

function updateNavbar () {
  if (window.scrollY > 75) {
    navbar.classList.add('nav-active')
    const storedTheme = localStorage.getItem('theme')
    navbar.setAttribute('data-bs-theme', storedTheme)
  } else {
    navbar.classList.remove('nav-active')
    const defaultTheme = navbar.getAttribute('data-bs-overlay')

    if (defaultTheme) {
      navbar.setAttribute('data-bs-theme', defaultTheme)
    }
  }
}

if ((navbar !== null) && (window.performance.getEntriesByType)) {
  if (window.performance.getEntriesByType('navigation')[0].type === 'reload') {
    fixed && updateNavbar()
  }
}

if (navbar !== null && togglers !== null) {
  // observe state changes to the site's color mode
  const html = document.querySelector('html')
  const config = {
    attributes: true,
    attributeFilter: ['data-bs-theme']
  }
  const Observer = new MutationObserver((mutationrecords) => {
    fixed && updateNavbar()
  })
  Observer.observe(html, config)

  // initialize background color
  const color = (navbar.getAttribute('data-navbar-color') || 'body')
  const bg = colorsBG.includes(color) ? `var(--bs-${color}-bg)` : `var(--bs-navbar-color-${color})`
  navbar.style.setProperty('--bs-navbar-expanded-color', bg)

  // set the navbar background color to opaque when scrolling past a breakpoint
  window.onscroll = () => {
    fixed && updateNavbar()
  }

  // set the navbar background color to opaque when expanded
  for (let i = 0; i < togglers.length; ++i) {
    togglers[i].onclick = () => {
      navbar.classList.toggle('navbar-expanded')
    }
  }

  // invoke the navbar toggler for each mode switcher to collapse the main menu afterwards
  for (let i = 0; i < modeSelectors.length; ++i) {
    modeSelectors[i].onclick = () => {
      for (let j = 0; j < togglers.length; ++j) {
        const toggler = togglers[j]
        if (toggler.getAttribute('aria-expanded') === 'true') {
          toggler.click()
        }
      }
    }
  }
}

;
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
// eslint-disable-next-line no-undef, no-unused-vars
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

;;
// Script to move all embedded toast messages into a container with id 'toast-container'. The container ensures multiple
// toast messages are stacked properly. The script targets all elements specified by a 'data-toast-target' and ensures
// the click event of the origin is linked as well.

const container = document.getElementById('toast-container')
if (container !== null) {
  // process all data-toast-target elements
  document.querySelectorAll('[data-toast-target]').forEach(trigger => {
    const target = document.getElementById(trigger.getAttribute('data-toast-target'))
    if (target !== null) {
      // move the element to the toast containr
      container.appendChild(target)

      // eslint-disable-next-line no-undef
      const toast = bootstrap.Toast.getOrCreateInstance(target)
      if (toast !== null) {
        // associate the click event of the origin with the toast element
        trigger.addEventListener('click', () => {
          toast.show()
        })
      }
    }
  })
}

;
// Bootstrap tooltip example: https://getbootstrap.com/docs/5.2/components/tooltips/
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
// eslint-disable-next-line no-unused-vars, no-undef
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

;
document.querySelectorAll('[data-video-padding]').forEach(element => {
  element.style.paddingBottom = element.getAttribute('data-video-padding')
})
