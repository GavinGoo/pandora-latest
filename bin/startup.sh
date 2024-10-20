#!/bin/bash

PANDORA_ARGS=""
PANDORA_COMMAND="pandora"
USER_CONFIG_DIR="/data"

# Set email, password, and mfa from environment variables if they are set
if [ -n "${OPENAI_EMAIL}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --email ${OPENAI_EMAIL}"
fi

if [ -n "${OPENAI_PASSWORD}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --password ${OPENAI_PASSWORD}"
fi

if [ -n "${OPENAI_MFA_CODE}" ]; then
  PANDORA_ARGS="${OPENAI_MFA_CODE} --mfa ${OPENAI_MFA_CODE}"
fi

if [ -n "${OPENAI_API_PREFIX}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --proxy_api ${OPENAI_API_PREFIX}"
fi

if [ -n "${OPENAI_LOGIN_URL}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --login_url ${OPENAI_LOGIN_URL}"
fi

if [ -n "${PANDORA_PROXY}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -p ${PANDORA_PROXY}"
fi

# Handle access token and tokens file
if [ -n "${PANDORA_ACCESS_TOKEN}" ]; then
  mkdir -p "${USER_CONFIG_DIR}"
  echo "${PANDORA_ACCESS_TOKEN}" >"${USER_CONFIG_DIR}/access_token.dat"
fi

if [ -n "${PANDORA_TOKENS_FILE}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --tokens_file ${PANDORA_TOKENS_FILE}"
fi

# Server mode
if [ -n "${PANDORA_SERVER}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -s ${PANDORA_SERVER}"
  if [ -n "${PANDORA_SITE_PASSWORD}" ]; then
    PANDORA_ARGS="${PANDORA_ARGS} --site_password ${PANDORA_SITE_PASSWORD}"
  fi
fi

# Model selection
if [ -n "${PANDORA_GPT4_MODEL}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --gpt4 ${PANDORA_GPT4_MODEL}"
fi

if [ -n "${PANDORA_GPT35_MODEL}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --gpt35 ${PANDORA_GPT35_MODEL}"
fi

# History settings
if [ -n "${PANDORA_HISTORY_COUNT}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --history_count ${PANDORA_HISTORY_COUNT}"
fi

if [ "${PANDORA_BEST_HISTORY}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --best_history"
fi

# Other options
if [ "${PANDORA_TRUE_DELETE}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --true_del"
fi

if [ "${PANDORA_LOCAL_OPTION}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -l"
fi

if [ -n "${PANDORA_TIMEOUT}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --timeout ${PANDORA_TIMEOUT}"
fi

if [ "${PANDORA_OAI_ONLY}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --oai_only"
fi

if [ "${PANDORA_OLD_LOGIN}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --old_login"
fi

if [ "${PANDORA_OLD_CHAT}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --old_chat"
fi

if [ -n "${PANDORA_FILE_SIZE}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --file_size ${PANDORA_FILE_SIZE}"
fi

if [ -n "${PANDORA_TYPE_WHITELIST}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --type_whitelist ${PANDORA_TYPE_WHITELIST}"
fi

if [ -n "${PANDORA_TYPE_BLACKLIST}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --type_blacklist ${PANDORA_TYPE_BLACKLIST}"
fi

if [ -n "${PANDORA_FILE_ACCESS}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --file_access ${PANDORA_FILE_ACCESS}"
fi

if [ -n "${OPENAI_DEVICE_ID}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --device_id ${OPENAI_DEVICE_ID}"
fi

if [ -n "${PANDORA_API}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -a"
fi

if [ -n "${PANDORA_LOGIN_LOCAL}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --login_local"
fi

if [ -n "${PANDORA_VERBOSE}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -v"
fi

if [ -n "${PANDORA_THREADS}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --threads ${PANDORA_THREADS}"
fi

if [ "${PANDORA_DEBUG}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --debug"
fi

if [ "${PANDORA_ISOLATION}" = "True" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} -i"
fi

if [ -n "${PANDORA_ISOLATION_MASTERCODE}" ]; then
  PANDORA_ARGS="${PANDORA_ARGS} --isolate_master ${PANDORA_ISOLATION_MASTERCODE}"
fi


if [ -n "${PANDORA_CLOUD}" ]; then
  PANDORA_COMMAND="pandora-cloud"
fi

export USER_CONFIG_DIR

# Execute the Pandora command with the arguments
# shellcheck disable=SC2086
$(command -v ${PANDORA_COMMAND}) ${PANDORA_ARGS}
