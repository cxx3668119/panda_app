type AnyFn = (...args: any[]) => any
type Timer = ReturnType<typeof setTimeout>

export interface Cancelable {
  cancel: () => void
}

export interface Flushable<T extends AnyFn> {
  flush: () => ReturnType<T> | undefined
}

export type DebouncedFn<T extends AnyFn> = ((
  ...args: Parameters<T>
) => ReturnType<T> | undefined) &
  Cancelable &
  Flushable<T>

export type ThrottledFn<T extends AnyFn> = ((
  ...args: Parameters<T>
) => ReturnType<T> | undefined) &
  Cancelable &
  Flushable<T>

export interface DebounceOptions {
  leading?: boolean
  trailing?: boolean
}

export interface ThrottleOptions {
  leading?: boolean
  trailing?: boolean
}

export const delay = (ms = 200) => new Promise((resolve) => setTimeout(resolve, ms))

export const sleep = delay

export function debounce<T extends AnyFn>(
  fn: T,
  wait = 300,
  options: DebounceOptions = {}
): DebouncedFn<T> {
  const { leading = false, trailing = true } = options
  let timer: Timer | undefined
  let lastArgs: Parameters<T> | undefined
  let lastThis: ThisParameterType<T> | undefined
  let lastResult: ReturnType<T> | undefined

  const invoke = () => {
    if (!lastArgs) return lastResult

    const args = lastArgs
    const context = lastThis
    lastArgs = undefined
    lastThis = undefined
    lastResult = fn.apply(context, args)
    return lastResult
  }

  const debounced = function (this: ThisParameterType<T>, ...args: Parameters<T>) {
    const shouldInvokeLeading = leading && !timer
    lastArgs = args
    lastThis = this

    if (timer) {
      clearTimeout(timer)
    }

    timer = setTimeout(() => {
      timer = undefined
      if (trailing) {
        invoke()
      }
    }, wait)

    if (shouldInvokeLeading) {
      return invoke()
    }

    return lastResult
  } as DebouncedFn<T>

  debounced.cancel = () => {
    if (timer) {
      clearTimeout(timer)
    }
    timer = undefined
    lastArgs = undefined
    lastThis = undefined
  }

  debounced.flush = () => {
    if (!timer) return lastResult

    clearTimeout(timer)
    timer = undefined
    return trailing ? invoke() : lastResult
  }

  return debounced
}

export function throttle<T extends AnyFn>(
  fn: T,
  wait = 300,
  options: ThrottleOptions = {}
): ThrottledFn<T> {
  const { leading = true, trailing = true } = options
  let timer: Timer | undefined
  let lastArgs: Parameters<T> | undefined
  let lastThis: ThisParameterType<T> | undefined
  let lastInvokeTime = 0
  let lastResult: ReturnType<T> | undefined

  const invoke = (time: number) => {
    if (!lastArgs) return lastResult

    const args = lastArgs
    const context = lastThis
    lastArgs = undefined
    lastThis = undefined
    lastInvokeTime = time
    lastResult = fn.apply(context, args)
    return lastResult
  }

  const startTimer = (remaining: number) => {
    timer = setTimeout(() => {
      timer = undefined
      if (trailing && lastArgs) {
        invoke(Date.now())
      }
    }, remaining)
  }

  const throttled = function (this: ThisParameterType<T>, ...args: Parameters<T>) {
    const now = Date.now()

    if (!lastInvokeTime && !leading) {
      lastInvokeTime = now
    }

    const remaining = wait - (now - lastInvokeTime)
    lastArgs = args
    lastThis = this

    if (remaining <= 0 || remaining > wait) {
      if (timer) {
        clearTimeout(timer)
        timer = undefined
      }
      return invoke(now)
    }

    if (!timer && trailing) {
      startTimer(remaining)
    }

    return lastResult
  } as ThrottledFn<T>

  throttled.cancel = () => {
    if (timer) {
      clearTimeout(timer)
    }
    timer = undefined
    lastArgs = undefined
    lastThis = undefined
    lastInvokeTime = 0
  }

  throttled.flush = () => {
    if (!timer) return lastResult

    clearTimeout(timer)
    timer = undefined
    return lastArgs ? invoke(Date.now()) : lastResult
  }

  return throttled
}

export function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max)
}

export function isNil(value: unknown): value is null | undefined {
  return value === null || value === undefined
}

export function noop() {
  // Empty utility for optional callbacks.
}

export function formatDate(
  value: string | number | Date,
  options: Intl.DateTimeFormatOptions = {},
  locale = 'zh-CN'
) {
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    ...options
  }).format(new Date(value))
}
