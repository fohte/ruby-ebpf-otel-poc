PUBLIC_IP = $(shell op plugin run -- aws ec2 describe-instances --filters "Name=tag:Name,Values=ebpf-sandbox" | jq -r '.Reservations[].Instances[].PublicIpAddress')
SSH_USERNAME := ec2-user

.PHONY: ssh
ssh:
	ssh $(SSH_USERNAME)@$(PUBLIC_IP)

.PHONY: deploy
deploy:
	rg --files | rsync -av --files-from=- . $(SSH_USERNAME)@$(PUBLIC_IP):~/poc
