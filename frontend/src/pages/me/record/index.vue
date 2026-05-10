<template>
  <main class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">record</div>
      <h1 class="page-title">个人档案</h1>
      <p class="page-subtitle">维护用于预测的个人信息。</p>
    </section>

    <section class="surface-card space-y-6">
      <ErrorRetryBox v-if="error">{{ error }}</ErrorRetryBox>
      <div v-else-if="success" class="info-box">{{ success }}</div>

      <div class="grid gap-4">
        <van-swipe-cell
          class="overflow-hidden rounded-3xl border border-line bg-white/80 shadow-soft"
          v-for="value in userStore.userRecords"
          :key="value.id"
        >
          <div
            class="flex min-h-20 items-center justify-between gap-3 overflow-hidden px-4 py-3"
          >
            <div class="min-w-0 flex-1 space-y-1.5 text-left">
              <div class="flex min-w-0 items-center gap-2">
                <span
                  class="max-w-[100px] truncate text-base font-semibold text-ink"
                  >{{ value.name }}</span
                >
                <span
                  class="inline-flex size-7 shrink-0 items-center justify-center rounded-full text-lg font-bold leading-none"
                  :class="genderIconClass(value.gender)"
                  :title="genderLabel(value.gender)"
                >
                  {{ genderIcon(value.gender) }}
                </span>
              </div>
              <div class="truncate text-sm leading-6 text-muted">
                {{ value.birthday }}
              </div>
            </div>

            <div class="flex shrink-0 items-center gap-3">
              <span
                class="rounded-full bg-accentSoft/75 px-3 py-1.5 text-xs font-semibold text-accentDeep"
              >
                {{ zodiacSignName(value) }}
              </span>
              <img
                class="size-10 shrink-0 rounded-full"
                :src="zodiacIcon(value.zodiac)"
                :alt="`${value.zodiac} zodiac icon`"
                :title="value.zodiac"
              />
            </div>
          </div>
          <template #right>
            <van-button square text="删除" type="danger" class="h-full" />
          </template>
        </van-swipe-cell>
      </div>

      <div class="flex flex-wrap gap-3">
        <button class="btn-primary" @click="handleClick('add')">新增</button>

        <RouterLink class="btn-ghost" to="/me">返回我的主页</RouterLink>
      </div>
    </section>

    <van-dialog
      v-model:show="infoDialogShow"
      title="新增"
      :before-close="beforeDialogClose"
      show-cancel-button
    >
      <van-form @submit="onSubmit" ref="formRef">
        <van-cell-group inset>
          <van-field
            v-model="newRecord.name"
            name="name"
            label="姓名"
            placeholder=""
            :rules="[{ required: true, message: '请输入姓名' }]"
          />
          <van-field name="gender" label="性别">
            <template #input>
              <van-radio-group
                v-model="newRecord.gender"
                direction="horizontal"
              >
                <van-radio name="male">男</van-radio>
                <van-radio name="female">女</van-radio>
              </van-radio-group>
            </template>
          </van-field>
          <van-field
            v-model="newRecord.birthday"
            is-link
            readonly
            name="datePicker"
            label="时间选择"
            placeholder="点击选择时间"
            :rules="[{ required: true, message: '请选择时间' }]"
            @click="showPicker = true"
          />
          <van-field
            v-model="newRecord.birthplace"
            is-link
            readonly
            name="area"
            label="地区选择"
            placeholder="点击选择省市区"
            @click="showArea = true"
          />
          <van-popup
            v-model:show="showArea"
            destroy-on-close
            position="bottom"
            teleport="body"
            :z-index="3200"
          >
            <van-area
              :area-list="areaList"
              :model-value="areaValue"
              @confirm="onAreaConfirm"
              @cancel="showArea = false"
            />
          </van-popup>
          <van-popup
            v-model:show="showPicker"
            destroy-on-close
            position="bottom"
            teleport="body"
            :z-index="3200"
          >
            <van-picker
              title="选择生辰"
              :columns="dateTimeColumns"
              :model-value="pickerValue"
              @change="onPickerChange"
              @confirm="onDateTimeConfirm"
              @cancel="showPicker = false"
            />
          </van-popup>
        </van-cell-group>
      </van-form>
    </van-dialog>
  </main>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import ErrorRetryBox from "@/components/common/ErrorRetryBox.vue";
import { useUserStore } from "@/stores/user";
import type { UserRecord } from "@/types";
import { throttle } from "@/utils";
import { areaList } from "@vant/area-data";

const userStore = useUserStore();
const error = ref("");
const success = ref("");
const infoDialogShow = ref(false);
const showPicker = ref(false);
const showArea = ref(false);
const pickerValue = ref<string[]>(getCurrentDateTimeValues());
const areaValue = ref("110101");
const formRef = ref();
const zodiacIconMap: Record<string, string> = {
  rat: "/zodiac/rat.png",
  mouse: "/zodiac/rat.png",
  ox: "/zodiac/ox.png",
  cow: "/zodiac/ox.png",
  tiger: "/zodiac/tiger.png",
  rabbit: "/zodiac/rabbit.png",
  dragon: "/zodiac/dragon.png",
  snake: "/zodiac/snake.png",
  horse: "/zodiac/horse.png",
  goat: "/zodiac/goat.png",
  sheep: "/zodiac/goat.png",
  monkey: "/zodiac/monkey.png",
  rooster: "/zodiac/rooster.png",
  chicken: "/zodiac/rooster.png",
  dog: "/zodiac/dog.png",
  pig: "/zodiac/pig.png",
  boar: "/zodiac/pig.png",
  鼠: "/zodiac/rat.png",
  牛: "/zodiac/ox.png",
  虎: "/zodiac/tiger.png",
  兔: "/zodiac/rabbit.png",
  龙: "/zodiac/dragon.png",
  蛇: "/zodiac/snake.png",
  马: "/zodiac/horse.png",
  羊: "/zodiac/goat.png",
  猴: "/zodiac/monkey.png",
  鸡: "/zodiac/rooster.png",
  狗: "/zodiac/dog.png",
  猪: "/zodiac/pig.png",
};
const newRecord = ref<UserRecord>({
  name: "",
  birthday: "",
  gender: "male",
  birthZodiacSign: "",
  birthplace: "",
  age: 1,
  zodiac: "",
  id: new Date().getTime(),
  horoscope: "",
});

type PickerOption = {
  text: string;
  value: string;
};

type PickerEventParams = {
  selectedValues: Array<string | number>;
};

type AreaConfirmParams = {
  selectedOptions: Array<
    { text?: string; name?: string; value?: string } | undefined
  >;
};

function pad(value: number | string) {
  return String(value).padStart(2, "0");
}

function getCurrentDateTimeValues() {
  const now = new Date();
  return [
    String(now.getFullYear()),
    pad(now.getMonth() + 1),
    pad(now.getDate()),
    pad(now.getHours()),
    pad(now.getMinutes()),
    pad(now.getSeconds()),
  ];
}

function createRangeOptions(
  start: number,
  end: number,
  suffix = "",
): PickerOption[] {
  return Array.from({ length: end - start + 1 }, (_, index) => {
    const value = suffix ? pad(start + index) : String(start + index);
    return {
      text: `${value}${suffix}`,
      value,
    };
  });
}

function getMonthDays(year: number, month: number) {
  return new Date(year, month, 0).getDate();
}

const dateTimeColumns = computed(() => {
  const [yearValue, monthValue] = pickerValue.value;
  const year = Number(yearValue) || new Date().getFullYear();
  const month = Number(monthValue) || 1;
  const dayCount = getMonthDays(year, month);

  return [
    createRangeOptions(1900, 2100, ""),
    createRangeOptions(1, 12, "月"),
    createRangeOptions(1, dayCount, "日"),
    createRangeOptions(0, 23, "时"),
    createRangeOptions(0, 59, "分"),
    createRangeOptions(0, 59, "秒"),
  ];
});

function normalizePickerValues(values: Array<string | number>) {
  const [year, month, day, hour, minute, second] = values.map(String);
  const dayCount = getMonthDays(Number(year), Number(month));
  return [
    year,
    pad(month),
    pad(Math.min(Number(day), dayCount)),
    pad(hour),
    pad(minute),
    pad(second),
  ];
}

function onPickerChange({ selectedValues }: PickerEventParams) {
  pickerValue.value = normalizePickerValues(selectedValues);
}

function normalizeValue(value: string) {
  return value.trim().toLowerCase();
}

function zodiacIcon(zodiac: string) {
  return zodiacIconMap[normalizeValue(zodiac)] || "/zodiac/rat.png";
}

function zodiacSignName(record: UserRecord) {
  return record.birthZodiacSign || record.horoscope;
}

function genderIcon(gender: string) {
  return normalizeValue(gender) === "female" || gender === "女" ? "♀" : "♂";
}

function genderLabel(gender: string) {
  return normalizeValue(gender) === "female" || gender === "女"
    ? "Female"
    : "Male";
}

function genderIconClass(gender: string) {
  return normalizeValue(gender) === "female" || gender === "女"
    ? "bg-[#fbefed] text-danger"
    : "bg-[#e8f0fb] text-[#2f68b0]";
}
const handleClick = throttle(
  (type: string) => {
    if (type === "add") {
      infoDialogShow.value = true;
    }
  },
  1000,
  { leading: true, trailing: false },
);
async function onSubmit() {
  console.log(newRecord.value);
}

async function beforeDialogClose(action: string) {
  if (action === "cancel") {
    return true;
  }

  try {
    await formRef.value?.validate();
    await onSubmit();
    return true;
  } catch {
    return false;
  }
}
function onDateTimeConfirm({ selectedValues }: PickerEventParams) {
  const [year, month, day, hour, minute, second] =
    normalizePickerValues(selectedValues);
  pickerValue.value = [year, month, day, hour, minute, second];
  newRecord.value.birthday = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
  showPicker.value = false;
}

function onAreaConfirm({ selectedOptions }: AreaConfirmParams) {
  const options = selectedOptions.filter(Boolean);
  const names = options.map((option) => option?.text || option?.name || "");
  const lastValue = options[options.length - 1]?.value;

  newRecord.value.birthplace = names.join(" ");
  if (lastValue) {
    areaValue.value = lastValue;
  }
  showArea.value = false;
}
</script>

<style scoped>
:deep(.van-swipe-cell__right) {
  height: 100%;
}

:deep(.van-swipe-cell__right .van-button) {
  height: 100%;
}
</style>
