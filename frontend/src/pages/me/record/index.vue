<template>
  <main class="page-shell">
    <section class="page-hero">
      <div class="eyebrow">Record</div>
      <h1 class="page-title">个人档案</h1>
      <p class="page-subtitle">维护用于预测的个人信息。</p>
    </section>

    <section class="surface-card space-y-6">
      <ErrorRetryBox v-if="error">{{ error }}</ErrorRetryBox>
      <div v-else-if="success" class="info-box">{{ success }}</div>

      <div v-if="userStore.userRecords.length" class="grid gap-4">
        <van-swipe-cell
          v-for="value in userStore.userRecords"
          :key="value.id"
          class="overflow-hidden rounded-3xl border border-line bg-white/80 shadow-soft"
          :before-close="(params) => beforeSwipeClose(value.id, params)"
        >
          <div
            class="flex min-h-20 items-center justify-between gap-3 overflow-hidden px-4 py-3"
            @click="openDetail(value)"
          >
            <div class="min-w-0 flex-1 space-y-1.5 text-left">
              <div class="flex min-w-0 items-center gap-2">
                <span class="max-w-[100px] truncate text-base font-semibold text-ink">
                  {{ value.name }}
                </span>
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
              <span class="rounded-full bg-accentSoft/75 px-3 py-1.5 text-xs font-semibold text-accentDeep">
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
      <div
        v-else
        class="rounded-3xl border border-dashed border-line bg-white/60 px-4 py-10 text-center text-sm text-muted"
      >
        暂无数据
      </div>

      <div class="flex flex-wrap gap-3">
        <button class="btn-primary" @click="openCreate">新增</button>
        <RouterLink class="btn-ghost" to="/me">返回我的主页</RouterLink>
      </div>
    </section>

    <van-dialog
      v-model:show="infoDialogShow"
      :title="dialogTitle"
      :before-close="beforeDialogClose"
      :show-confirm-button="dialogMode !== 'view'"
      :show-cancel-button="dialogMode !== 'view'"
      confirm-button-text="保存"
      cancel-button-text="取消"
    >
      <van-form ref="formRef" @submit="onSubmit">
        <van-cell-group v-if="dialogMode === 'view'" inset>
          <van-field :model-value="editingRecord.name" readonly label="姓名" />
          <van-field :model-value="genderText(editingRecord.gender)" readonly label="性别" />
          <van-field :model-value="editingRecord.birthday" readonly label="生辰" />
          <van-field :model-value="editingRecord.birthplace" readonly label="地区" />
          <van-field :model-value="String(editingRecord.age)" readonly label="年龄" />
          <van-field :model-value="editingRecord.zodiac" readonly label="属相" />
          <van-field :model-value="editingRecord.horoscope" readonly label="星座" />
          <van-field :model-value="editingRecord.birthZodiacSign" readonly label="生辰八字" />
        </van-cell-group>

        <van-cell-group v-else inset>
          <van-field
            v-model="editingRecord.name"
            name="name"
            label="姓名"
            placeholder="请输入姓名"
            :rules="[{ required: true, message: '请输入姓名' }]"
          />
          <van-field name="gender" label="性别">
            <template #input>
              <van-radio-group v-model="editingRecord.gender" direction="horizontal">
                <van-radio name="male">男</van-radio>
                <van-radio name="female">女</van-radio>
              </van-radio-group>
            </template>
          </van-field>
          <van-field
            v-model="editingRecord.birthday"
            is-link
            readonly
            name="birthday"
            label="生辰"
            placeholder="点击选择生辰"
            :rules="[{ required: true, message: '请选择生辰' }]"
            @click="showPicker = true"
          />
          <van-field
            v-model="editingRecord.birthplace"
            is-link
            readonly
            name="birthplace"
            label="地区"
            placeholder="点击选择省市区"
            :rules="[{ required: true, message: '请选择地区' }]"
            @click="showArea = true"
          />
        </van-cell-group>
      </van-form>

      <template v-if="dialogMode === 'view'" #footer>
        <div class="grid grid-cols-2 border-t border-line">
          <button class="dialog-action dialog-action-cancel" type="button" @click="infoDialogShow = false">
            关闭
          </button>
          <button class="dialog-action dialog-action-confirm" type="button" @click="switchToEdit">
            修改
          </button>
        </div>
      </template>
    </van-dialog>

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
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { areaList } from "@vant/area-data";
import { showFailToast, showSuccessToast } from "vant";
import ErrorRetryBox from "@/components/common/ErrorRetryBox.vue";
import { addRecord, deleteRecord, updateRecord } from "@/api/record";
import { useUserStore } from "@/stores/user";
import type { UserRecord } from "@/types";

const userStore = useUserStore();
const error = ref("");
const success = ref("");
const infoDialogShow = ref(false);
const showPicker = ref(false);
const showArea = ref(false);
const dialogMode = ref<"create" | "view" | "edit">("create");
const formRef = ref();
const pickerValue = ref<string[]>(getCurrentDateTimeValues());
const areaValue = ref("110101");
const editingRecord = ref<UserRecord>(createEmptyRecord());
const dialogTitle = computed(() => {
  if (dialogMode.value === "create") return "新增";
  if (dialogMode.value === "view") return "档案详情";
  return "修改档案";
});

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

type PickerOption = {
  text: string;
  value: string;
};

type PickerEventParams = {
  selectedValues: Array<string | number>;
};

type AreaConfirmParams = {
  selectedOptions: Array<{ text?: string; name?: string; value?: string } | undefined>;
};

onMounted(() => {
  userStore.getUserRecords().catch((err) => {
    error.value = err instanceof Error ? err.message : "Failed to load records.";
  });
});

function createEmptyRecord(): UserRecord {
  return {
    id: Date.now(),
    name: "",
    birthday: "",
    gender: "male",
    birthZodiacSign: "",
    birthplace: "",
    age: 1,
    zodiac: "",
    horoscope: "",
  };
}

function openCreate() {
  dialogMode.value = "create";
  editingRecord.value = createEmptyRecord();
  pickerValue.value = getCurrentDateTimeValues();
  areaValue.value = "110101";
  infoDialogShow.value = true;
}

function openDetail(record: UserRecord) {
  dialogMode.value = "view";
  editingRecord.value = { ...record };
  syncPickerFromBirthday(record.birthday);
  infoDialogShow.value = true;
}

function switchToEdit() {
  dialogMode.value = "edit";
}

async function onSubmit() {
  if (dialogMode.value === "create") {
    await addRecord(editingRecord.value);
    showSuccessToast("记录添加成功");
  } else {
    await updateRecord(editingRecord.value);
    showSuccessToast("记录修改成功");
  }
  await userStore.getUserRecords();
}

async function beforeDialogClose(action: string) {
  if (dialogMode.value === "view") {
    return true;
  }

  if (action === "cancel") {
    return true;
  }

  try {
    await formRef.value?.validate();
    await onSubmit();
    return true;
  } catch (err) {
    showFailToast(err instanceof Error ? err.message : "保存失败，请稍后重试");
    return false;
  }
}

async function beforeSwipeClose(
  recordId: number,
  { position }: { event: Event; name: string; position: string },
) {
  if (position !== "right") {
    return true;
  }

  try {
    await deleteRecord(recordId);
    showSuccessToast("删除成功");
    await userStore.getUserRecords();
    return true;
  } catch (err) {
    showFailToast(err instanceof Error ? err.message : "删除失败，请稍后重试");
    return false;
  }
}

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

function syncPickerFromBirthday(value: string) {
  const match = value.match(/^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})/);
  pickerValue.value = match ? match.slice(1, 7) : getCurrentDateTimeValues();
}

function createRangeOptions(start: number, end: number, suffix = ""): PickerOption[] {
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
    createRangeOptions(1900, 2100),
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

function onDateTimeConfirm({ selectedValues }: PickerEventParams) {
  const [year, month, day, hour, minute, second] = normalizePickerValues(selectedValues);
  pickerValue.value = [year, month, day, hour, minute, second];
  editingRecord.value.birthday = `${year}-${month}-${day} ${hour}:${minute}:${second}`;
  showPicker.value = false;
}

function onAreaConfirm({ selectedOptions }: AreaConfirmParams) {
  const options = selectedOptions.filter(Boolean);
  const names = options.map((option) => option?.text || option?.name || "");
  const lastValue = options[options.length - 1]?.value;

  editingRecord.value.birthplace = names.join(" ");
  if (lastValue) {
    areaValue.value = lastValue;
  }
  showArea.value = false;
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
  return normalizeValue(gender) === "female" || gender === "女" ? "Female" : "Male";
}

function genderText(gender: string) {
  return normalizeValue(gender) === "female" || gender === "女" ? "女" : "男";
}

function genderIconClass(gender: string) {
  return normalizeValue(gender) === "female" || gender === "女"
    ? "bg-[#fbefed] text-danger"
    : "bg-[#e8f0fb] text-[#2f68b0]";
}
</script>

<style scoped>
:deep(.van-swipe-cell__right) {
  height: 100%;
}

:deep(.van-swipe-cell__right .van-button) {
  height: 100%;
}

.dialog-action {
  min-height: 48px;
  background: #fff;
  font-size: 14px;
  font-weight: 500;
}

.dialog-action-cancel {
  color: #667067;
}

.dialog-action-confirm {
  color: #5f7f62;
}
</style>
