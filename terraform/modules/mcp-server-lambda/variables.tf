variable "source_name" {
  type        = string
  description = "The source of the lambda, this should be the directory name inside src/ using underscores, e.g. test_lambda"
}

variable "function_name" {
  type        = string
  description = "The name of the lambda function, usually local name plus source name combined"
}

variable "runtime" {
  type        = string
  description = "The lambda runtime to use, e.g. python3.12 or nodejs22.x"
}

variable "account_id" {
  type        = string
  description = "The account ID"
  sensitive   = true
}

variable "entrypoint" {
  type        = string
  description = "The function entrypoint"
}

variable "memory_size" {
  type        = number
  description = "The memory to allocate to the lambda"
  default     = 128
}
